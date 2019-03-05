import vtk
import numpy as np


def get_sphere_actors(pos, rad):
    source = vtk.vtkSphereSource()
#    source.SetResolution(10)
    source.SetCenter(pos)
    source.SetRadius(rad)
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    return actor


def get_sphered_obstacle(data):
    
    data_temp = np.loadtxt(path_directory + obj_type + '.txt', delimiter = ',')

    num_cols = int(data.shape[1])
    pos = (0,0,0)
    
    