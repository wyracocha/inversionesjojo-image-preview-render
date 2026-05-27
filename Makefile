# Previene que Git Bash (MSYS2) convierta rutas como /data/... a C:/Program Files/...
export MSYS_NO_PATHCONV=1

# Parámetros para generate_image_render (pasar con VAR=valor al ejecutar make)
STL     ?= modelo.stl   # Nombre del archivo .stl dentro del contenedor
OUT_DIR ?= /output      # Carpeta de salida dentro del contenedor

generate_image_render:
	@echo "stl: $(STL)"
	docker run \
		--rm \
		-e TZ=America/Lima \
		-v "$(STL):/data/model.stl" \
		-v "$(PWD)/main.py:/data/main.py" \
		-v "$(PWD)/output:/data/output" \
		lscr.io/linuxserver/blender:latest blender -b -P /data/main.py -- /data/model.stl /data/output
generate_video_render:
	docker run \
		--rm \
		-e TZ=America/Lima \
		-v "$(PWD)/output:/data/output" \
		linuxserver/ffmpeg \
		-y \
		-framerate 24 \
		-i "/data/output/frame_%04d.png" \
		-c:v libx264 \
		-preset slow \
		-crf 18 \
		-pix_fmt yuv420p \
		/data/output/render_360.mp4
all: generate_image_render generate_video_render
