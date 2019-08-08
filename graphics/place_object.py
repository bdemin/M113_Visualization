import numpy as np

from vtk import vtkTransform, vtkMatrix4x4, vtkTransformPolyDataFilter

from graphics.transformations import trans_matrix, rot_matrix


def place_all_bodies(data, timer_count):
    for obj_index in range(len(data)):
        for _object in data[obj_index]:
            _object.Move(_object.path_loc[timer_count],
                _object.path_dir[timer_count])
            place_object(_object.actor,
                _object.position,
                _object.angles)    


def place_object(actor, new_pos, angles):
    matrix = np.matmul(trans_matrix(*new_pos) , rot_matrix(*angles))
    trans = vtkTransform()
    vtk_matrix = vtkMatrix4x4()
    m, n = matrix.shape
    for i in range(m):
        for j in range(n):
            vtk_matrix.SetElement(i,j,matrix[i][j])
    trans.SetMatrix(vtk_matrix)
    transformFilter = vtkTransformPolyDataFilter()
    transformFilter.SetTransform(trans)
    actor.SetUserTransform(trans)
    