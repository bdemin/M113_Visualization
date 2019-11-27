import numpy as np
from os import listdir

from bodies.helpers import create_bodies
from graphics.visualize import visualize

from helpers.functions import get_directory
from simulation_description import show_description


path = '../M113_tests/Data_Movies/'
# directory = path + 'Step/' + 'Step0.7_A/'
directory = path + 'Slope/' + 'Slope31deg_Friction0.55/'
# directory = path + 'Brake/' + 'Brake10__VeryLowFriction/'
# directory = path + 'OverSteering/' + 'OverSterring_LowFriction 10ms/'
# directory = path + 'Turning/' + 'TurningRadius_30Deg/'

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

if 'Slope' in directory or 'OverSteering' in directory:
    # Temporary fix for chassis position
    x_add = 0.12
    x_offset = -1.9888 - chassis[0].path_loc[0,0] + x_add

    for body in chassis:
        body.path_loc[480:,:] = body.path_loc[479,:]
        body.path_dir[480:,:] = body.path_dir[479,:]
    for body in road_wheels:
        body.path_loc[480:,:] = body.path_loc[479,:]
        body.path_dir[480:,:] = body.path_dir[479,:]
    for body in trailing_arms:
        body.path_loc[480:,:] = body.path_loc[479,:]
        body.path_dir[480:,:] = body.path_dir[479,:]
    for body in sprockets:
        body.path_loc[480:,:] = body.path_loc[479,:]
        body.path_dir[480:,:] = body.path_dir[479,:]
    for body in idlers:
        body.path_loc[480:,:] = body.path_loc[479,:]
        body.path_dir[480:,:] = body.path_dir[479,:]
    for body in track_units:
        body.path_loc[480:,:] = body.path_loc[479,:]
        body.path_dir[480:,:] = body.path_dir[479,:]
    # chassis[0].path_loc[:,0] += x_offset

    # chassis[0].path_loc[:,2] -= 0.04

# Fix rotations
for idler in idlers:
    idler.path_dir[:,1] = sprockets[0].path_dir[:,1]
for road_wheel in road_wheels:
    road_wheel.path_dir[:,1] = sprockets[0].path_dir[:,1]

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
