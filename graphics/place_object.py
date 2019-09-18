import numpy as np

from vtk import vtkTransform, vtkMatrix4x4, vtkTransformPolyDataFilter

from graphics.transformations import trans_matrix, rot_matrix


def place_all_bodies(data, timer_count):
    for bodies in data:
        for body in bodies:
            body.Move(body.path_loc[timer_count],
                body.path_dir[timer_count])
            place_body(body, data[0][0])
    
def place_body(body, chassis = None):
    # if body.type == 'Idler' and body.side == 'R':
        # print(np.linalg.norm(body.position - chassis.position))

    trans = vtkTransform()
    trans.Identity()

    trans.Translate(body.position)

    trans.RotateX(np.rad2deg(chassis.angles[0]))
    trans.RotateY(np.rad2deg(chassis.angles[1]))
    trans.RotateZ(np.rad2deg(chassis.angles[2]))

    # if body.type == 'Chassis':
    #     trans.RotateX(np.rad2deg(body.angles[0]))
    #     trans.RotateY(np.rad2deg(body.angles[1]))
    #     trans.RotateZ(np.rad2deg(body.angles[2]))
    
    # # elif body.type in ['Idler', 'Sprocket', 'Road_Wheel', 'Track']:
    # else:
    #     if body.side == 'L':
    #         rotation_dir_vec = chassis.actor.GetMatrix().MultiplyPoint((0,1,0,0))[0:3]
    #     else:
    #         rotation_dir_vec = chassis.actor.GetMatrix().MultiplyPoint((0,-1,0,0))[0:3]
    #     # trans.RotateWXYZ(np.rad2deg(body.angles[1]), rotation_dir_vec)
        
    #     trans.RotateX(np.rad2deg(chassis.angles[0]))
    #     trans.RotateY(np.rad2deg(chassis.angles[1]))
    #     trans.RotateZ(np.rad2deg(chassis.angles[2]))
    
    body.actor.SetUserTransform(trans)

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
