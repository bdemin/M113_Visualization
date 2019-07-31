def keyboard_events(obj, pause, camera_flag):
    key = obj.GetKeySym()

    if key == 'o' and pause == False:
        pause = True
    elif key == 'o':
        pause = False
        
    if key == 'i' and camera_flag == True:
        camera_flag = False
    elif key == 'i':
        camera_flag = True
        
    return pause, camera_flag
    