import numpy as np


def place_camera(time, data, camera, camera_distance, view):
    # Define camera parameters
    
    camera.SetViewUp([0,0,1])

    if view == 1:
        # General view
        chs_pos = data[0][0].path_loc[time] # Chassis CG @ time
        cam_d = 12 # [m]
        cam_h = 4.5 # [m]
        chs2cam = [2 , -cam_d, cam_h] # vector from chassis to camera position
        chs_fix = [0,0,0]
        camera_pos = chs_pos + chs2cam

        cam_focal_point = chs_pos

    elif view == 2:
        # Rear view
        chassis_pos = data[0][0].path_loc[time] # Chassis CG @ time
        chs2cam = [-7,0,-0.5]
        # camera_pos = chassis_pos + chs2cam

        # Cam direction is locked on the chassis
        chassis_dir = data[0][0].path_dir[time]
        cam_d = 10
        camera_pos = chassis_pos + [-cam_d*np.cos(chassis_dir[2]), -cam_d*np.sin(chassis_dir[2]), cam_d*np.sin(chassis_dir[1]) + 1.5]
        camera.Roll(np.rad2deg(chassis_dir[0]))

        cam_focal_point = chassis_pos

    elif view == 3:
        # Wheel view
        wheel_pos = data[1][7].path_loc[time] # Wheel #7 CG @ time

        # Cam direction is locked on the wheel
        wheel_dir = data[1][7].path_dir[time]
        cam_d = 1.5
        camera_pos = wheel_pos + [cam_d*np.sin(wheel_dir[2]), -cam_d*np.cos(wheel_dir[2]), -np.sin(wheel_dir[0]) + 0.2]

        cam_focal_point = wheel_pos
        # camera_pos = wheel_pos + [0,-1.6,0.1]

    elif view == 4:
        # Top view
        chassis_pos = data[0][0].path_loc[time] # Chassis CG @ time
        chassis_dir = data[0][0].path_dir[time]

        cam_d = 10
        camera_pos = chassis_pos + [0.001,0.001,cam_d]
        cam_focal_point = chassis_pos
        # camera.Roll(np.rad2deg(chassis_dir[2]))

    elif view == 5:
        # Cool side view test
        chassis_pos = data[0][0].path_loc[time] # Chassis CG @ time
        chs2cam = [-7,0,-0.5]
        camera_pos = chassis_pos + chs2cam

        # Cam direction is locked on the chassis
        chassis_dir = data[0][0].path_dir[time]
        cam_d = 7

        cam_focal_point = chassis_pos + [cam_d*np.sin(chassis_dir[2]), -cam_d*np.cos(chassis_dir[2]), -np.sin(chassis_dir[0]) + 0.2]
    
    # Place camera and set focal point:
    camera.SetPosition(camera_pos)
    camera.SetFocalPoint(cam_focal_point)