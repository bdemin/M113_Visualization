def get_latest_directory(path):
    # Function to return latest folder inside path
    from os import listdir
    folder_list = listdir(path)
    folder_list = sorted([folder for folder in folder_list])
    if folder_list:
        return path + folder_list[-1] + '/'
    return None
