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

        # camera.SetRoll(slope)
        # camera.SetRoll(31)

    elif view == 2:
        # General view
        chs_pos = data[0][0].path_loc[time] # Chassis CG @ time
        cam_d = 12 # [m]
        cam_h = 4.5 # [m]
        chs2cam = [2 , -cam_d, cam_h] # vector from chassis to camera position
        chs_fix = [0,0,0]
        camera_pos = chs_pos + chs2cam

        cam_focal_point = chs_pos

    elif view == 3:
        # Rear view
        chassis_pos = data[0][0].path_loc[time] # Chassis CG @ time
        chs2cam = [-9,0,3]
        # camera_pos = chassis_pos + chs2cam

        # Cam direction is locked on the chassis
        chassis_dir = data[0][0].path_dir[time]
        cam_d = 10
        # camera_pos = chassis_pos + [-cam_d*np.cos(chassis_dir[2]), -cam_d*np.sin(chassis_dir[2]), cam_d*np.sin(chassis_dir[1]) + 2.5]
        camera_pos = chassis_pos + chs2cam
        camera.Roll(np.rad2deg(chassis_dir[0]))

        cam_focal_point = chassis_pos


    elif view == 4:
        # For turning simulation
        camera.SetViewUp([0,0,1])

        chs_pos = data[0][0].path_loc[time] # Chassis CG @ time
        chs2cam = [0 , -20, 5] # vector from chassis to camera position
        camera_pos = chs_pos + chs2cam

        cam_focal_point = chs_pos
        
        # Place camera and set focal point:
        camera.SetPosition(camera_pos)
        camera.SetFocalPoint(cam_focal_point)

        # camera.SetRoll(slope)
        camera.SetRoll(15)

    elif view == 5:
        camera.SetViewUp([0,0,1])

        # cam_focal_point = data[0][0].path_loc[-1] + [-2,0,0]
        cam_focal_point = data[0][0].path_loc[-1] + [-7,0,0]
        # camera_pos = cam_focal_point + [-1.5,-15,0]
        camera_pos = cam_focal_point + [-4 * 1.3,-15 * 1.3,0]
        camera.SetDistance(20)
        
        # Place camera and set focal point:
        camera.SetPosition(camera_pos)
        camera.SetFocalPoint(cam_focal_point)

        # camera.SetRoll(slope)
        # camera.SetRoll(31)

    # Place camera and set focal point:
    camera.SetPosition(camera_pos)
    camera.SetFocalPoint(cam_focal_point)
    