# Fix conditionals

def keyboard_events(obj, callback):
    key = obj.GetKeySym()
    if key == 'o' and callback.pause == False:
        callback.pause = True
    elif key == 'o':
        callback.pause = False
        
    if key == 'i' and callback.camera.is_on:
        callback.camera.is_on = False
    elif key == 'i':
        callback.camera.is_on = True
        
    if key == 'u' and callback.camera.is_on:
        callback.camera.distance += 1
    if key == 'y' and callback.camera.is_on:
        callback.camera.distance -= 1

    if key == 'v':
        if callback.camera.current_view == 'isometric':
            callback.camera.current_view = 'general'
        elif callback.camera.current_view == 'general':
            callback.camera.current_view = 'rear'
        elif callback.camera.current_view == 'rear':
            callback.camera.current_view = 'top'
        else:
            callback.camera.current_view = 'isometric'
        print(f'Camera set to: {callback.camera.current_view} view')

    if key == 'bracketright':
        # check if there is enough time
        callback.timer_count += 10
    elif key == 'bracketleft':
        if callback.timer_count > 10:
            callback.timer_count -= 10

    if key == 'backslash':
        callback.timer_count = 0

    if key == 'j':
        callback.camera.dolly_factor += 1
    elif key == 'h':
        callback.camera.dolly_factor -= 1
