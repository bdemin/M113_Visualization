def keyboard_events(obj, pause, camera_flag, camera_distance, view, timer):
    key = obj.GetKeySym()
    print(key)
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

    if pause:
        if key == 'bracketright':
            timer += 10
        elif key == 'bracketleft':
            if timer > 10:
                timer -= 10

    if key == 'backslash':
        timer = 0


    # Add camera zoom
    if key == 'equal':
        pass
    if key == 'minus':
        pass
        

    return pause, camera_flag, camera_distance, view, timer
    