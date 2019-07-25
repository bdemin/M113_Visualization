import numpy as np


def place_camera(camera, chs_pos, chs_ang):
    # Define camera parameters
    view = 3
    if view == 1:
        # General view
        cam_d = 14 #[m]
        cam_h = 5 #[m]
        chs2cam = [2 , -cam_d, cam_h]

    elif view == 2:
        # Rear view
        cam_d = 14
        cam_h = 1
        chs2cam = [-15,0,0]

    elif view == 3:
        # Wheel view
        cam_d = 14 #[m]
        cam_h = 0
        chs2cam = [0,-2,0]

    camera_pos = chs_pos + chs2cam

    # place camera and set focal point:
    camera.SetViewUp([0,0,1])
    camera.SetPosition(camera_pos)
    camera.SetFocalPoint(chs_pos)