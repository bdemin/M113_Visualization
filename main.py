import numpy as np

from bodies.helpers import create_bodies
from graphics.visualize import visualize

from base_classes import SpheredRock
from simulation_description import show_description


path_directory = '../M113_tests/Data_Movies/3d_Rocks1/'
show_description(path_directory)

#%% Create bodies
chassis = create_bodies(path_directory, 'Chassis')
road_wheels = create_bodies(path_directory, 'Road_Wheel', side = True)
trailing_arms = create_bodies(path_directory, 'Trailing_Arm', side = True)
sprockets = create_bodies(path_directory, 'Sprocket', side = True)
idlers = create_bodies(path_directory, 'Idler', side = True)
track_units = create_bodies(path_directory, 'Track_Unit')

# Test trailing arm
offset = 0.2
for arm in trailing_arms:
    if arm.side == 'L':
        arm.path_loc[:,1] -= offset
    else:
        arm.path_loc[:,1] += offset

        
#%% Visualize
# Load time data
total_time = np.loadtxt(path_directory + 'Time_Data.txt', delimiter = ',')

# Visualize all bodies
visualize(chassis, road_wheels, trailing_arms, sprockets, idlers, track_units,
            path_directory = path_directory, total_time = total_time)

# Visualize specific bodies
# visualize(chassis, road_wheels, sprockets, idlers, track_units, obstacles, total_time = total_time, path_directory = path_directory)
