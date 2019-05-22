import numpy as np


def place_camera(camera, chs_pos, chs_ang):
    # define camera parameters:
    cam_d = 12
    cam_h = 5
    chs2cam = [cam_d*np.sin(chs_ang[2]), -cam_d*np.cos(chs_ang[2]), cam_h]
    camera_pos = chs_pos + chs2cam

    # place camera and set focal point:
    camera.SetViewUp([0,0,1])
    camera.SetPosition(camera_pos)
    camera.SetFocalPoint(chs_pos) 