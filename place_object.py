import numpy as np

from vtk import vtkTransform, vtkMatrix4x4, vtkTransformPolyDataFilter


def trans_matrix(dx, dy, dz):
    matrix = np.eye(4)
    matrix[0,3] = dx
    matrix[1,3] = dy
    matrix[2,3] = dz
    return matrix

def rot_matrix(a3, a2, a1):
    sin = np.sin
    cos = np.cos
    matrix = []
    matrix.append(cos(a1)*cos(a2))
    matrix.append(cos(a1)*sin(a2)*sin(a3) - sin(a1)*cos(a3))
    matrix.append(cos(a1)*sin(a2)*cos(a3) + sin(a1)*sin(a3))
    matrix.append(0)
    
    matrix.append(sin(a1)*cos(a2))
    matrix.append(sin(a1)*sin(a2)*sin(a3) + cos(a1)*cos(a3))
    matrix.append(sin(a1)*sin(a2)*cos(a3) - cos(a1)*sin(a3))
    matrix.append(0)
    
    matrix.append(-sin(a2))
    matrix.append(cos(a2)*sin(a3))
    matrix.append(cos(a2)*cos(a3))
    matrix.append(0)
    
    matrix.append(0)
    matrix.append(0)
    matrix.append(0)
    matrix.append(1)
    
    matrix = np.asarray(matrix).reshape(4,4)
    return matrix
    
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
    
def scale_actor(actor, factor, prev_trans = None):
    transform = vtkTransform()
    if prev_trans != None:
        transform.Concatenate(prev_trans)
    transform.Scale(tuple(3*[factor]))
    transformFilter = vtkTransformPolyDataFilter()
    transformFilter.SetTransform(transform)
    actor.SetUserTransform(transform)
    return transform #can be improved
