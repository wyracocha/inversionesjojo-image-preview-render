import sys
import os
import subprocess


def find_ffmpeg():
    """Busca ffmpeg en el PATH del sistema."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        if result.returncode == 0:
            return "ffmpeg"
    except FileNotFoundError:
        pass
    return None


def main():
    """
    Genera un video MP4 a partir de una carpeta de frames PNG.

    Uso:
        python render.py <carpeta_frames> [video_salida]

    Argumentos:
        carpeta_frames  Carpeta que contiene los archivos frame_0000.png, frame_0001.png, ...
        video_salida    (Opcional) Ruta del archivo MP4 de salida.
                        Por defecto: <carpeta_frames>/render_360.mp4
    """
    if len(sys.argv) < 2:
        print("Uso: python render.py <carpeta_frames> [video_salida]")
        print("  carpeta_frames : carpeta con los PNG generados por main.py")
        print("  video_salida   : (opcional) ruta del MP4 de salida")
        return

    frames_dir = sys.argv[1]
    video_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(frames_dir, "render_360.mp4")

    # Validar que la carpeta existe y tiene frames
    if not os.path.isdir(frames_dir):
        print(f"Error: La carpeta '{frames_dir}' no existe.")
        return

    frames = sorted([f for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".png")])
    if not frames:
        print(f"Error: No se encontraron archivos frame_*.png en '{frames_dir}'.")
        return

    print(f"  Carpeta de frames : {frames_dir}")
    print(f"  Frames encontrados: {len(frames)}")
    print(f"  Video de salida   : {video_path}")

    # Buscar ffmpeg
    ffmpeg = find_ffmpeg()
    if ffmpeg is None:
        print("\nAVISO: ffmpeg no encontrado. Instálalo y agrégalo al PATH.")
        print("Puedes crear el video manualmente con:")
        print(f"  ffmpeg -framerate 24 -i \"{frames_dir}/frame_%04d.png\" -c:v libx264 -pix_fmt yuv420p \"{video_path}\"")
        return

    # Generar MP4 con ffmpeg
    cmd = [
        ffmpeg,
        "-y",                       # Sobreescribir si existe
        "-framerate", "24",
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",               # Calidad alta (0=sin pérdida, 51=peor)
        "-pix_fmt", "yuv420p",      # Compatibilidad máxima con reproductores
        video_path
    ]

    print(f"\nEjecutando ffmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"\n✓ Video generado correctamente.")
        print(f"  Frames PNG : {frames_dir}/frame_*.png")
        print(f"  Video MP4  : {video_path}")
    else:
        print(f"\n✗ Error al generar el video con ffmpeg:")
        print(result.stderr[-2000:])


if __name__ == "__main__":
    main()
