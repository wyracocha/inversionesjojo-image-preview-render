# Documentación del Script de Renderizado 360°

Este script (`main.py`) automatiza el proceso de importación de modelos 3D (STL/OBJ), configuración de iluminación, renderizado de una rotación de 360 grados en imágenes PNG y la generación final de un video MP4.

## Requisitos del Sistema

Para ejecutar este script correctamente, es necesario tener instalados los siguientes componentes:

### 1. Blender
El script utiliza la API interna de Blender (`bpy`), por lo que debe ejecutarse utilizando el ejecutable de Blender.
- **Descarga:** [blender.org/download](https://www.blender.org/download/)
- **Versión recomendada:** 3.0 o superior (compatible con `wm.stl_import` y `wm.obj_import`).

### 2. FFmpeg
Utilizado para convertir la secuencia de imágenes PNG en un archivo de video MP4.
- **Instalación en Windows:**
  1. Descarga los binarios desde [ffmpeg.org](https://ffmpeg.org/download.html) o usa un gestor de paquetes como `choco install ffmpeg`.
  2. Asegúrate de añadir la carpeta `bin` de FFmpeg a las **Variables de Entorno (PATH)** del sistema.
  - *Nota: El script también intentará buscar `ffmpeg.exe` dentro de la carpeta donde esté instalado Blender.*

## Archivos Necesarios

1. **`main.py`**: El script principal de procesamiento.
2. **Modelo 3D**: Archivo en formato `.stl` o `.obj` que se desea renderizar.

## Instrucciones de Ejecución

El script se debe ejecutar desde la terminal (CMD o PowerShell) pasando los argumentos a Blender en modo "background" (`-b`).

### Sintaxis básica:
```bash
blender -b -P "main.py" -- "ruta/al/modelo.stl" ["carpeta_de_salida"]
```

### Ejemplo:
```bash
blender -b -P "C:\Users\NOSTROMO\Downloads\main.py" -- "C:\Users\NOSTROMO\Downloads\mi_modelo.stl"
```

## Detalles del Proceso
1. **Limpieza:** Se eliminan todos los objetos existentes en la escena.
2. **Importación:** Se carga el modelo y se centra automáticamente en el origen (0,0,0).
3. **Iluminación:** Se configura un esquema de 3 puntos de luz (Key, Fill, Rim) para resaltar los detalles del modelo.
4. **Renderizado:** Se generan 36 cuadros (frames) en formato PNG.
5. **Video:** FFmpeg une los cuadros en un archivo llamado `render_360.mp4` a 24 fps.

## Solución de Problemas
- **Error: 'blender' no se reconoce...**: Asegúrate de que la ruta al ejecutable de Blender esté en tu PATH o usa la ruta completa (ej. `"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"`).
- **FFmpeg no encontrado**: Si el script termina sin generar el video, instala FFmpeg y reinicia la terminal.
