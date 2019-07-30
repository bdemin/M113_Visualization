def keyboard_events(obj, pause, camera_flag):
    key = obj.GetKeySym()
    if key == 'o':
        pause = True
        
    elif key == 'i':
        pause = False
    
    elif key == 'u':
        camera_flag = False
        
    elif key == 'y':
        camera_flag = True
        
    return pause, camera_flag
    