def keyboard_events(obj, pause, camera_flag, camera_distance, view):
    key = obj.GetKeySym()

    if key == 'o' and pause == False:
        pause = True
    elif key == 'o':
        pause = False
        
    if key == 'i' and camera_flag:
        camera_flag = False
    elif key == 'i':
        camera_flag = True
        
    if key == 'u' and camera_flag:
        camera_distance += 1
    if key == 'y' and camera_flag:
        camera_distance -= 1

    if key == 'v':
        if view == 1:
            view = 2
        elif view == 2:
            view = 3
        else:
            view = 1

    return pause, camera_flag, camera_distance, view
    