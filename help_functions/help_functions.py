import numpy as np

from vtk import vtkSTLReader, vtkPolyDataMapper, vtkActor, vtkSphereSource


def find_angle(x0, y0):
    return np.arctan(y0/x0)*180/np.pi+90

def get_stl_actor(filename):
    reader = vtkSTLReader()
    reader.SetFileName(filename)
    
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    
    actor = vtkActor()
    actor.SetMapper(mapper)
    
    return actor