import numpy as np
from os import listdir

from graphics.visualize import visualize

from helpers.functions import get_directory



path = '../M113_tests/Data_Movies/'
directory = get_directory(path)





# Test trailing arm
offset = 0.1
for arm in trailing_arms:
    if arm.side == 'L':
        arm.path_loc[:,1] += offset
    else:
        arm.path_loc[:,1] -= offset

#%% Visualize
# Load time data
total_time = np.loadtxt(directory + 'Time_Data.txt', delimiter = ',')

# Visualize all bodies
visualize(chassis, road_wheels, trailing_arms, sprockets, idlers, track_units,
            directory = directory, total_time = total_time)

# Visualize specific bodies
# visualize(chassis, road_wheels, sprockets, idlers, track_units, obstacles, total_time = total_time, directory = directory)
