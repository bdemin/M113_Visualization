import numpy as np
from os import listdir, path


class DataModifier(object):
    # Class to manipulate and fix data files before entering visualization pipeline

    def __init__(self, directory = None):
        self.dir = directory
        if not self.dir:
            self.dir = '../M113_tests/Data_Movies/'

    def latest_by_date(self):
        # Function to return latest folder by creation date

        files = listdir(self.dir)
        paths = [path.join(self.dir, basename) for basename in files]
        if paths:
            # return max(paths, key=path.getctime).split('/')[-1]
            self.working_folder = max(paths, key=path.getctime).split('/')[-1]
            return
        raise FileNotFoundError('No simulation data found in: ' + self.dir)

    def latest_by_name(self):
        # Function to return latest folder by datetime format

        folder_names = []
        folders = listdir(self.dir)
        for folder_name in folders:
            folder_names.append(int(folder_name.replace(' ', '-').replace('-', '')))
        if folder_names:
            ind = np.argmax(folder_names)
            # return folders[ind]
            self.working_folder = folders[ind] + '/'
            return
        raise FileNotFoundError('No simulation data found in: ' + self.dir)

    def load_data(self):
        self.data = {}
        txt_files = listdir(self.dir + '/' + self.working_folder + '/')
        for txt_file in txt_files:
            self.data[txt_file.split('.')[0]] = np.loadtxt(self.dir + self.working_folder + txt_file, delimiter=',')

    def reverse_rotation(self): # Needed
        pass
        # X rotation direction for track_units
        # for track_unit in track_units:
            # track_unit.path_dir[:,0] *= -1

    def offset_y(self, body_type):
        
        # Trailing arm y offset
        # offset = 0.0
        # for arm in trailing_arms:
        #     if arm.side == 'L':
        #         arm.path_loc[:,1] += offset
        #     else:
        #         arm.path_loc[:,1] -= offset

    def save_data(self, directory):
        for file in self.data:
            np.savetxt(directory + str(file), file, delimiter=',')

save_directory = 'input_data/'
directory = '../M113_tests/Data_Movies/'

dm = DataModifier(directory)
res = dm.latest_by_name()
dm.load_data()