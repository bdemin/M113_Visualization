from os import listdir
from collections import OrderedDict


def get_latest_directory(path):
    # Function to return latest folder by date inside path
    
    folder_list = listdir(path)
    if folder_list:
        date_dict = dict([(date, date.replace(' ', '-').split('-')) for date in folder_list])

        # date_dict = sorted(date_dict.values(), key=lambda d: tuple(map(int, d.split('-'))))
        # date_dict = dict((date, date.split()))
        # date_dict2 = OrderedDict(sorted(date_dict.items(), key=lambda d: tuple(map(int, d[1].split('-')))))
        # folder_list = [folder.replace(' ', '-') for folder in folder_list]
        # folder_list = dict( [folder.replace(' ', '-') for folder in date_dict.values()]
        
        
        
        print(folder_list[-1])
        return path + folder_list[-1] + '/'
    raise FileNotFoundError('No simulation data found in: ' + path)
