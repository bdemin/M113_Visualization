def get_stl_actor(filename):
    # Retrive VTKActor pointing to STL file described in filename
    from vtk import vtkSTLReader, vtkPolyDataMapper, vtkActor, vtkSphereSource
    reader = vtkSTLReader()
    reader.SetFileName(filename)
    
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    
    actor = vtkActor()
    actor.SetMapper(mapper)
    
    return actor

def get_directory(path):
    # Function to return latest folder directory inside path
    from os import listdir
    folder_list = listdir(path)
    if folder_list:
        folder_list = sorted([folder for folder in folder_list])
        print(folder_list[-1])
        return path + folder_list[-1] + '/'
    print('Folder has no simulation data.')
    exit()
    