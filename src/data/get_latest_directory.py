from os import listdir
from re import sub


def get_latest_directory(path):
    # Function to return latest folder by date inside path
    
    folder_list = listdir(path)
    if folder_list:
        date_dict = dict([(date, int(sub('[^0-9]', '', date))) for date in folder_list])
        date_dict = {k: v for k, v in sorted(date_dict.items(), key=lambda item:item[1])}

        print('Visualizing data from folder: ', folder_list[-1])
        return path + list(date_dict.keys())[-1] + '/'
    raise FileNotFoundError('No simulation data found in: ' + path)
