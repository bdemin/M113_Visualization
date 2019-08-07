import numpy as np


def place_camera(time, data, camera, camera_distance, view):
    # Define camera parameters

    if view == 1:
        # General view
        chs_pos = data[0][0].path_loc[time] # Chassis CG @ time
        cam_d = 14 # [m]
        cam_h = 5 # [m]
        chs2cam = [2 , -cam_d, cam_h] # vector from chassis to camera position
        chs_fix = [0,0,0]
        camera_pos = chs_pos + chs2cam

        cam_focal_point = chs_pos

    elif view == 2:
        # Rear view
        chs_pos = data[0][0].path_loc[time] # Chassis CG @ time
        chs2cam = [-7,0,-0.5]
        chs_fix = [0,0,0]
        camera_pos = chs_pos + chs2cam

        cam_focal_point = chs_pos

    elif view == 3:
        # Wheel view
        wheel_pos = data[1][7].path_loc[time] # Wheel #7 CG @ time
        cam_focal_point = wheel_pos
        camera_pos = wheel_pos + [0,-3,0]
    
    # Place camera and set focal point:
    camera.SetViewUp([0,0,1])
    camera.SetPosition(camera_pos)
    camera.SetFocalPoint(cam_focal_point)