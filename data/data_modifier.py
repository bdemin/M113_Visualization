import numpy as np
from os import listdir


class DataModifier(object):
    def __init__(self, directory):
        files = listdir(directory)

    def load_data(self, filename):
        self.data = np.loadtxt(filename + '.txt', delimiter=',')

    def reverse_rotation(self): # Needed
        pass
        # X rotation direction for track_units
        # for track_unit in track_units:
            # track_unit.path_dir[:,0] *= -1

    def offset_y(self):
        pass
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


directory = 'data/raw_input/'
save_directory = 'data/input/'
dm = DataModifier(directory)
