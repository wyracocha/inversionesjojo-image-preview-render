# Renderizado 360° de Modelos 3D

Genera una animación de 360° a partir de un modelo 3D (STL/OBJ) en dos pasos independientes:

1. **`main.py`** — Renderiza los frames PNG usando Blender dentro de un contenedor Docker.
2. **`render.py`** — Ensambla los frames en un video MP4 usando FFmpeg.

---

## Requisitos

| Herramienta | Uso | Instalación |
|-------------|-----|-------------|
| **Docker** | Corre Blender para generar los frames | [docs.docker.com](https://docs.docker.com/get-docker/) |

> La imagen Docker `lscr.io/linuxserver/blender:latest` incluye Blender y se descarga automáticamente en el primer uso.

> [!IMPORTANT]
> **Usuarios de Windows:** Los comandos del `Makefile` (y `make` en general) funcionan mejor si los ejecutas desde **WSL** (Windows Subsystem for Linux).
> El `Makefile` usa `$(PWD)` y sintaxis de montaje de volúmenes que son nativas de shells Unix.
> Si los ejecutas desde PowerShell o CMD podrías tener problemas con las rutas y los volúmenes de Docker.
>
> ```bash
> # Abre tu terminal WSL y navega al proyecto, por ejemplo:
> cd /my-directory
> make generate_image_render STL=tests/capibara-stl.stl
> ```

---

## Estructura esperada del proyecto

```
inversionesjojo-image-preview-render/
├── main.py          # Script de renderizado (corre dentro de Docker)
├── render.py        # Script de ensamblado de video (corre en el host)
├── Makefile
├── tests/
│   └── capibara-stl.stl   # Modelos de prueba
└── output/          # Carpeta generada automáticamente con los frames PNG
```

---

## Paso 1 — Generar los frames PNG

Usa el target `generate_image_render` del Makefile. El modelo debe estar dentro del proyecto (ruta relativa desde la raíz).

### Sintaxis
```bash
make generate_image_render STL=<ruta/relativa/al/modelo.stl>
```

### Ejemplo
```bash
make generate_image_render STL=tests/capibara-stl.stl
```

Esto ejecuta Blender en Docker con los siguientes volúmenes montados:

| Host | Contenedor | Descripción |
|------|-----------|-------------|
| `$(PWD)/$(STL)` | `/data/model.stl` | Archivo del modelo |
| `$(PWD)/main.py` | `/data/main.py` | Script de renderizado |
| `$(PWD)/output/` | `/data/output` | Carpeta de salida de frames |

### Resultado
```
output/
  frame_0000.png
  frame_0001.png
  ...
  frame_0035.png
```

---

## Paso 2 — Generar el video MP4

Usa el target `generate_video_render` del Makefile. Lee los frames de la carpeta `output/` y genera el archivo `render_360.mp4` en la misma carpeta.

### Sintaxis
```bash
make generate_video_render
```

No requiere parámetros — siempre lee de `./output/` y escribe en `./output/render_360.mp4`.

### Resultado
```
output/
  frame_0000.png
  frame_0001.png
  ...
  frame_0035.png
  render_360.mp4   ← generado por este comando
```

> Usa la imagen `linuxserver/ffmpeg` en Docker, por lo que no necesitas FFmpeg instalado en el host.

---

## Todo en un solo paso (`make all`)

Si deseas ejecutar tanto la generación de frames como el ensamblado del video de manera secuencial, puedes usar el target `all` del `Makefile`.

### Sintaxis
```bash
make all STL=<ruta/relativa/al/modelo.stl>
```

### Ejemplo
```bash
make all STL=tests/capibara-stl.stl
```

Este comando renderiza los frames en la carpeta `output/` e inmediatamente después usa FFmpeg para ensamblarlos en `render_360.mp4`, simplificando todo el flujo.

---

## Parámetros del video generado

| Parámetro    | Valor     | Descripción                                      |
|--------------|-----------|--------------------------------------------------|
| Codec        | `libx264` | H.264, amplia compatibilidad con reproductores   |
| Framerate    | `24 fps`  | Velocidad de reproducción                        |
| CRF          | `18`      | Alta calidad (0 = sin pérdida, 51 = mínima)      |
| Pixel format | `yuv420p` | Máxima compatibilidad (VLC, Windows Media, etc.) |
| Preset       | `slow`    | Mejor compresión al mismo nivel de calidad       |

---

## Detalles del proceso de renderizado (`main.py`)

1. **Limpieza:** Se eliminan todos los objetos existentes en la escena de Blender.
2. **Importación:** Se carga el modelo y se centra automáticamente en el origen `(0, 0, 0)`.
3. **Iluminación:** Esquema de 3 puntos de luz:
   - **Key (principal):** Frontal-derecha, elevación 45°, energía 3.
   - **Fill (relleno):** Izquierda, altura media, energía 1.5.
   - **Rim (contorno):** Trasera, ligeramente abajo, energía 2.
4. **Cámara:** Orbita alrededor del modelo a distancia `max_dim × 3.5`.
5. **Frames:** 36 imágenes PNG (una cada 10° de rotación).

---

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| `Cannot connect to the Docker daemon` | Asegúrate de que Docker Desktop esté corriendo. |
| `No se encontraron archivos frame_*.png` | Verifica que el Paso 1 haya completado sin errores y que la carpeta `output/` exista. |
| `FFmpeg no encontrado` | Instala FFmpeg y reinicia la terminal para que el PATH se actualice. |
| Formato no soportado | Solo se aceptan archivos `.stl` y `.obj`. |
