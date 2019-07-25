import numpy as np


def place_camera(camera, chs_pos, chs_ang):
    # define camera parameters:
    cam_d = 14 #[m]
    # cam_h = 5 #[m]
    cam_h = 1
    cam_angle = np.arcsin(cam_h/cam_d) # [rad]
    cam_h = cam_d * np.sin(cam_angle)
    
    # chs2cam = [cam_d*np.sin(chs_ang[2]), -cam_d*np.cos(chs_ang[2]), cam_h]
    chs2cam = [2 , -cam_d, cam_h]
    # chs2cam = [-15,0,0]
    camera_pos = chs_pos + chs2cam

    # place camera and set focal point:
    camera.SetViewUp([0,0,1])
    camera.SetPosition(camera_pos)
    camera.SetFocalPoint(chs_pos)