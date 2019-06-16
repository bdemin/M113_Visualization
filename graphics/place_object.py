import numpy as np

from vtk import vtkTransform, vtkMatrix4x4, vtkTransformPolyDataFilter

from graphics.transformations import trans_matrix, rot_matrix

    
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
    

