# def keyboard_events(obj, pause, camera.is_on, camera_distance, view, timer):
def keyboard_events(obj, pause, camera, timer):
    key = obj.GetKeySym()
    if key == 'o' and pause == False:
        pause = True
    elif key == 'o':
        pause = False
        
    if key == 'i' and camera.is_on:
        camera.is_on = False
    elif key == 'i':
        camera.is_on = True
        
    if key == 'u' and camera.is_on:
        camera.distance += 1
    if key == 'y' and camera.is_on:
        camera.distance -= 1

    if key == 'v':
        if view == 'isometric':
            view = 2
        elif view == 2:
            view = 3
        else:
            view = 'isometric'

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
        

    return pause, camera.is_on, camera_distance, view, timer
    