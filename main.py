import bpy
import math
import sys
import os



def main():
    # Obtener argumentos después de "--"
    try:
        args = sys.argv[sys.argv.index("--") + 1:]
        input_model = args[0]
        # Si no se da carpeta, crear una basada en el nombre del modelo
        if len(args) > 1:
            output_dir = args[1]
        else:
            output_dir = os.path.join(
                os.getcwd(),
                os.path.splitext(os.path.basename(input_model))[0] + "_render"
            )
    except (IndexError, ValueError):
        print("Uso: blender -b -P 360.py -- <modelo> [carpeta_salida]")
        return

    # 1. Limpiar escena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # 2. Importar modelo
    if not os.path.exists(input_model):
        print(f"Error: El archivo '{input_model}' no existe.")
        return

    ext = os.path.splitext(input_model)[1].lower()
    if ext == ".stl":
        bpy.ops.wm.stl_import(filepath=input_model)
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=input_model)
    else:
        print(f"Error: Formato '{ext}' no soportado.")
        return

    obj = bpy.context.selected_objects[0]

    # 3. Centrar objeto
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    obj.location = (0, 0, 0)

    # 4. Configurar Cámara y Luz
    max_dim = max(obj.dimensions)
    dist = max_dim * 3.5

    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam

    tt = cam.constraints.new(type='TRACK_TO')
    tt.target = obj
    tt.track_axis = 'TRACK_NEGATIVE_Z'
    tt.up_axis = 'UP_Y'

    # Luz principal (key) — frontal-derecha, elevación ~45°
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    key = bpy.context.active_object
    key.data.energy = 3
    key.rotation_euler = (math.radians(45), 0, math.radians(-45))

    # Luz de relleno (fill) — izquierda, a la altura de la cintura
    bpy.ops.object.light_add(type='SUN', location=(-5, -3, 0))
    fill = bpy.context.active_object
    fill.data.energy = 1.5
    fill.rotation_euler = (math.radians(90), 0, math.radians(135))

    # Luz trasera (rim) — detrás y ligeramente abajo, da contorno
    bpy.ops.object.light_add(type='SUN', location=(0, -5, -3))
    rim = bpy.context.active_object
    rim.data.energy = 2
    rim.rotation_euler = (math.radians(120), 0, math.radians(180))

    # 5. Configurar Render de imágenes
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    n_frames = 12

    os.makedirs(output_dir, exist_ok=True)

    # 6. Bucle de Renderizado (360 grados) - Frame por frame
    print(f"\nRenderizando {n_frames} frames en: {output_dir}")
    for i in range(n_frames):
        angle = (i / n_frames) * 2 * math.pi
        cam.location.x = math.cos(angle) * dist
        cam.location.y = math.sin(angle) * dist
        cam.location.z = 0

        frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
        scene.render.filepath = frame_path
        bpy.ops.render.render(write_still=True)
        print(f"  Frame {i+1:02d}/{n_frames} -> {os.path.basename(frame_path)}")



if __name__ == "__main__":
    main()
