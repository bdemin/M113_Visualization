import numpy as np
from os import listdir

from bodies.helpers import create_bodies
from graphics.visualize import visualize

from helpers.functions import get_directory
from simulation_description import show_description


path = '../M113_tests/Data_Movies/'
directory = get_directory(path)

show_description(directory)

#%% Create bodies
chassis = create_bodies(directory, 'Chassis')
road_wheels = create_bodies(directory, 'Road_Wheel', side = True)
trailing_arms = create_bodies(directory, 'Trailing_Arm', side = True)
sprockets = create_bodies(directory, 'Sprocket', side = True)
idlers = create_bodies(directory, 'Idler', side = True)
track_units = create_bodies(directory, 'Track_Unit')

#%% Temporary fixes for the visualization
# X rotation direction for track_units
for track_unit in track_units:
    track_unit.path_dir[:,0] *= -1

for trailing_arm in trailing_arms:
    if trailing_arm.side == 'L':
        trailing_arm.path_dir[:, 1] *= -1

# Trailing arm y offset
offset = 0.0
for arm in trailing_arms:
    if arm.side == 'L':
        arm.path_loc[:,1] += offset
    else:
        arm.path_loc[:,1] -= offset

# sprockets[0].path_dir[:,1] *= -1
# idlers[0].path_dir[:,1] *= -1

# road_wheels[7].actor.GetProperty().SetOpacity(0.4)


#%% Visualize
# Load time data
total_time = np.loadtxt(directory + 'Time_Data.txt', delimiter = ',')

# Visualize all bodies
visualize(chassis, road_wheels, sprockets, idlers, track_units,
            directory = directory, total_time = total_time)

# Visualize specific bodies
# visualize(chassis, road_wheels, sprockets, idlers, track_units, obstacles, total_time = total_time, directory = directory)
