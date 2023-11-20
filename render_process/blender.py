import bpy


def update_blender_file(file_path, points):
       
    try:
        print('Starting script')
        bpy.ops.wm.open_mainfile(filepath=file_path)
    except Exception as e:
        print(f'Error opening file: {e}')
        try:
            print('Creating new file')
            bpy.ops.wm.read_factory_settings(use_empty=True)
            print('Blender file path invalid. Creating new file of the same name')
        except Exception as e:
            print(f'Error creating new file: {e}')
            return -1
    
    print('File opened')
    
    try:
        # Create a new mesh
        mesh = bpy.data.meshes.new(name="Points")
        obj = bpy.data.objects.new(name="Points_Object", object_data=mesh)
        bpy.context.collection.objects.link(obj)

        # Add the points to the mesh
        mesh.from_pydata(points, [], [])

        # Update the mesh
        mesh.update()
    except Exception as e:
        print(f'Error in point updation: {e}')
        return -2
    
    scene = bpy.context.scene

    try:
        bpy.ops.wm.save_as_mainfile(filepath=file_path)
    except Exception as e: 
        print(f'Error in file save: {e}')
        return -3
    
    return 0


if __name__ == '__main__':
    file_path = "D:\Anirudh\Projects\DARTS Rover Dashboard\existing_blend_file.blend"
    i=2
    x=0
    points =[(1+x, 1,i), (1+x, -1, i), (-1+x, -1, i), (-1+x, 1, i)]  # Example points
    update_blender_file(file_path, points)