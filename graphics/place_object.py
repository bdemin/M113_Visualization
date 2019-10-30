import numpy as np

from vtk import vtkTransform, vtkMatrix4x4, vtkTransformPolyDataFilter, \
    vtkMath

from graphics.transformations import trans_matrix, rot_matrix


def place_all_bodies(data, timer_count):
    for bodies in data:
        for body in bodies:
            if body.type == 'Chassis':
                body.Move(body.path_loc[timer_count],
                        body.path_dir[timer_count])
                place_body(body)
            else:
                body.Move(body.path_loc[timer_count],
                    body.path_dir[timer_count])
                place_body(body, data[0][0])

def place_body(body, chassis = None):
    body.trans.Identity()
    body.trans.PreMultiply()
    body.trans.Translate(body.position)

    if body.side == 'L':
        chassis_angles = (chassis.angles[0], chassis.angles[1], chassis.angles[2] - np.pi)
        rotating_angles = (0, -body.angles[1], 0)
    elif body.side == 'R':
        chassis_angles = chassis.angles[:]
        rotating_angles = (0, body.angles[1], 0)
    elif body.type == 'Chassis':
        chassis_angles = body.angles

    body.trans.RotateX(np.rad2deg(chassis_angles[0]))
    body.trans.RotateY(np.rad2deg(chassis_angles[1]))
    body.trans.RotateZ(np.rad2deg(chassis_angles[2]))
    

    if body.type != 'Chassis':
        body.trans.RotateX(np.rad2deg(rotating_angles[0]))
        body.trans.RotateY(np.rad2deg(rotating_angles[1]))
        body.trans.RotateZ(np.rad2deg(rotating_angles[2]))
            
    
    body.actor.SetUserTransform(body.trans)

    # if side == 'L':
    #     first_angles = (-chassis_angles[0], chassis_angles[1], chassis_angles[2]-np.pi)
    #     y_rotation = (0, -angles[1], 0)
    # elif side == 'R':
    #     first_angles = chassis_angles[:]
    #     y_rotation = (0, angles[1], 0)
    
    # rotations_matrix = np.matmul(rot_matrix(*(first_angles[0],0,first_angles[2])), rot_matrix(*y_rotation))

    # final_matrix = np.matmul(trans_matrix(*new_pos), rotations_matrix)
    # trans = vtkTransform()
    # vtk_matrix = vtkMatrix4x4()
    # m, n = final_matrix.shape
    # for i in range(m):
    #     for j in range(n):
    #         vtk_matrix.SetElement(i,j,final_matrix[i][j])
    # trans.SetMatrix(vtk_matrix)
    # transformFilter = vtkTransformPolyDataFilter()
    # transformFilter.SetTransform(trans)
    # actor.SetUserTransform(trans)
