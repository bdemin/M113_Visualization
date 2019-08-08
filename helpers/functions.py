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
    # Function to return latest folder inside path
    from os import listdir
    folder_list = listdir(path)
    folder_list = sorted([folder for folder in folder_list])

    return path + folder_list[-1] + '/'
