import numpy as np

from vtk import vtkTransform, vtkTransformPolyDataFilter


def trans_matrix(dx, dy, dz):
    matrix = np.eye(4)
    matrix[0,3] = dx
    matrix[1,3] = dy
    matrix[2,3] = dz
    return matrix

def rot_matrix(x, y, z):
    # [,,;...
    # ;];

    sin = np.sin
    cos = np.cos
    matrix = []

    Cx = cos(x)
    Cy = cos(y)
    Cz = cos(z)

    Sx = sin(x)
    Sy = sin(y)
    Sz = sin(z)

    matrix.append(Cy * Cz)
    matrix.append(Cz * Sx * Sy-Cx * Sz)
    matrix.append(Sx * Sz+Cx * Cz * Sy)
    matrix.append(0)
    
    matrix.append(Cy * Sz)
    matrix.append(Cx * Cz+Sx * Sy * Sz)
    matrix.append(Cx * Sy * Sz-Cz * Sx)
    matrix.append(0)
    
    matrix.append(-Sy)
    matrix.append(Cy * Sx)
    matrix.append(Cx * Cy)
    matrix.append(0)
    
    matrix.append(0)
    matrix.append(0)
    matrix.append(0)
    matrix.append(1)
    
    matrix = np.asarray(matrix).reshape(4,4)
    return matrix


def scale_actor(actor, factor, prev_trans = None):
    transform = vtkTransform()
    if prev_trans != None:
        transform.Concatenate(prev_trans)
    transform.Scale(tuple(3*[factor]))
    transformFilter = vtkTransformPolyDataFilter()
    transformFilter.SetTransform(transform)
    actor.SetUserTransform(transform)
    return transform #can be improved