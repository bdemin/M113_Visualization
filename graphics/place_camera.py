import numpy as np


def place_camera(time, data, camera, camera_distance, view, slope):
    # Define camera parameters
    
    camera.SetViewUp([0,0,1])

    if view == 1:
        camera.SetViewUp([0,0,1])

        chs_pos = data[0][0].path_loc[time] # Chassis CG @ time
        chs2cam = [0 , -20, 0] # vector from chassis to camera position
        camera_pos = chs_pos + chs2cam

        cam_focal_point = chs_pos
        
        # Place camera and set focal point:
        camera.SetPosition(camera_pos)
        camera.SetFocalPoint(cam_focal_point)

        # factor = 0.005
        # roll_angle = time * factor
        camera.SetRoll(slope)

    elif view == 2:
        # General view
        chs_pos = data[0][0].path_loc[time] # Chassis CG @ time
        cam_d = 12 # [m]
        cam_h = 4.5 # [m]
        chs2cam = [2 , -cam_d, cam_h] # vector from chassis to camera position
        chs_fix = [0,0,0]
        camera_pos = chs_pos + chs2cam

        cam_focal_point = chs_pos
    
    # Place camera and set focal point:
    camera.SetPosition(camera_pos)
    camera.SetFocalPoint(cam_focal_point)
    