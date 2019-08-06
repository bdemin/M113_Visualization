import numpy as np


def place_camera(camera, chs_pos, chs_ang):
    # Define camera parameters
    view = 1
    if view == 1:
        # General view
        cam_d = 14 # [m]
        cam_h = 5 # [m]
        chs2cam = [2 , -cam_d, cam_h] # vector from chassis to camera position
        chs_fix = [0,0,0]
        camera_pos = chs_pos + chs2cam

    elif view == 2:
        # Rear view
        chs2cam = [-12,0,0]
        chs_fix = [0,0,0]
        camera_pos = chs_pos + chs2cam

    elif view == 3:
        # Wheel view
        chs2cam = [0,-4,0]
        chs_fix = [0,0,-1]
        camera_pos = chs_pos + chs2cam + chs_fix
    
    # Place camera and set focal point:
    camera.SetViewUp([0,0,1])
    camera.SetPosition(camera_pos)
    camera.SetFocalPoint(chs_pos + chs_fix)