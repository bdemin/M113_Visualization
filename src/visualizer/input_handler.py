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
        if camera.current_view == 'isometric':
            camera.current_view = 'general'
        elif camera.current_view == 'general':
            camera.current_view = 'rear'
        elif camera.current_view == 'rear':
            camera.current_view = 'top'
        else:
            camera.current_view = 'isometric'
        print(f'Camera set to: {camera.current_view} view')

    if key == 'bracketright':
        # check if there is enough time
        timer += 10
    elif key == 'bracketleft':
        if timer > 10:
            timer -= 10

    if key == 'backslash':
        timer = 0

    if key == 'j':
        camera.dolly_factor += 1
    elif key == 'h':
        camera.dolly_factor -= 1

    return pause, timer
    