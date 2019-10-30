import numpy as np

from vtk import vtkTransform, vtkMatrix4x4, vtkTransformPolyDataFilter

from graphics.transformations import trans_matrix, rot_matrix


def place_all_bodies(data, timer_count):
    data[0][0].Move(data[0][0].path_loc[timer_count],
                data[0][0].path_dir[timer_count])

    place_chassis(data[0][0].actor,
                data[0][0].position,
                data[0][0].angles)

    for obj_index in range(1,len(data) - 1):
        for _object in data[obj_index]:
            _object.Move(_object.path_loc[timer_count],
                _object.path_dir[timer_count])
            place_object(_object.actor,
                _object.position,
                _object.angles,
                data[0][0].path_dir[timer_count],
                _object.side)

    for link in data[-1]:
        link.Move(link.path_loc[timer_count],
            link.path_dir[timer_count])
        place_chassis(link.actor,
                link.position,
                link.angles)


def place_object(actor, new_pos, angles, chassis_angles, side):
    if side == 'L':
        first_angles = (chassis_angles[0], chassis_angles[1], chassis_angles[2]-np.pi)
        y_rotation = (0, -angles[1], 0)
    elif side == 'R':
        first_angles = chassis_angles[:]
        y_rotation = (0, angles[1], 0)
    
    trans = vtkTransform()
    trans.PreMultiply()
    trans.Translate(*new_pos)
    
    trans.RotateX(np.rad2deg(first_angles[0]))
    trans.RotateY(np.rad2deg(first_angles[1]))
    trans.RotateZ(np.rad2deg(first_angles[2]))
    
    trans.RotateX(np.rad2deg(y_rotation[0]))
    trans.RotateY(np.rad2deg(y_rotation[1]))
    trans.RotateZ(np.rad2deg(y_rotation[2]))

    actor.SetUserTransform(trans)


def place_chassis(actor, new_pos, angles):
    matrix = np.matmul(trans_matrix(*new_pos) , rot_matrix(*angles))
    trans = vtkTransform()
    vtk_matrix = vtkMatrix4x4()
    m, n = matrix.shape
    for i in range(m):
        for j in range(n):
            vtk_matrix.SetElement(i, j, matrix[i][j])

    trans.SetMatrix(vtk_matrix)
    transformFilter = vtkTransformPolyDataFilter()
    transformFilter.SetTransform(trans)
    actor.SetUserTransform(trans)
    
