import numpy as np

from base_classes import Chassis, Road_Wheel, Sprocket, Idler, Track_Unit, Obstacle
from base_classes import Sphered_Rock
from draw_system import draw_system
from simulation_description import show_description


dataFile = 'M113_STL.xlsx'
# path_directory = 'INPUT/Simulation_5/'
path_directory = 'C:/Users/bdemin/Documents/GitHub/M113_tests/Data_Movies/Simulation_5/'
show_description(path_directory)

#%%create Chassis object:
chassis = []
obj_type = 'Chassis'
path_data = np.loadtxt(path_directory + obj_type + '.txt', delimiter = ',')
path_loc = path_data[:,0:3]
path_dir = path_data[:,3:6]
chassis.append(Chassis(path_loc, path_dir))

#%%create Road_Wheel objects:
road_wheels = []
obj_type = 'Road_Wheel'
path_data = np.loadtxt(path_directory + obj_type + '.txt', delimiter = ',')

num_cols = int(path_data.shape[1])
for wheel_index in range(0, num_cols, 6):
    path_loc = []
    path_dir = []
    loc_slice = slice(wheel_index, wheel_index+3)
    path_loc = path_data[:,loc_slice]
    path_dir = np.asarray(list(chassis[0].path_dir))
    if path_loc[0][1] > 0:
        side = 'L'
        path_dir[:,2] += np.pi
    else:
        side = 'R'
    road_wheels.append(Road_Wheel(side,
                                  path_loc,
                                  path_dir))

#%%create Sprocket objects:
sprockets = []
obj_type = 'Sprocket'
path_data = np.loadtxt(path_directory + obj_type + '.txt', delimiter = ',')
num_cols = int(path_data.shape[1])
for sprocket_index in range(0, num_cols, 6):
    path_loc = []
    path_dir = []
    loc_slice = slice(sprocket_index, sprocket_index+3)
    dir_slice = slice(sprocket_index+3, sprocket_index+6)
    path_loc = path_data[:,loc_slice]
    path_dir = path_data[:,dir_slice]
    if path_loc[0][1] > 0:
        side = 'L'
        path_dir[:,2] += np.pi
    else:
        side = 'R'
    sprockets.append(Sprocket(side,
                                  path_loc,
                                  path_dir))
    
    
#%%create Idler objects:
idlers = []
obj_type = 'Idler'
path_data = np.loadtxt(path_directory + obj_type + '.txt', delimiter = ',')
num_cols = int(path_data.shape[1])
for idler_index in range(0, num_cols, 6):
    path_loc = []
    loc_slice = slice(idler_index, idler_index+3)
    path_loc = path_data[:,loc_slice]
    path_dir = sprockets[int(idler_index/6)].path_dir
    if path_loc[0][1] > 0:
        side = 'L'
    else:
        side = 'R'
    idlers.append(Idler(side, path_loc, path_dir))

#%%create Track_Unit objects:
track_units = []
obj_type = 'Track_Unit'
position_data = np.loadtxt(path_directory + obj_type + '.txt', delimiter = ',')

#calculate directions:
position_data_L, position_data_R = np.split(position_data, 2, axis = 1)
direction_data_L = np.roll(position_data_L, 3, axis=1) - position_data_L
direction_data_R = np.roll(position_data_R, 3, axis=1) - position_data_R
direction_data = np.concatenate((direction_data_L, direction_data_R), axis = 1)


num_cols = int(position_data.shape[1])
for track_unit_index in range(0, num_cols, 3):
    path_loc = []
    path_dir = []
    _slice = slice(track_unit_index, track_unit_index+3)
    path_loc = position_data[:, _slice]
    path_dir = np.asarray(list(chassis[0].path_dir))
    y_angle = np.arctan2(direction_data[:,track_unit_index], direction_data[:,track_unit_index+2])
    path_dir[:,1] = np.deg2rad(90) + y_angle
    track_units.append(Track_Unit(path_loc, path_dir))

    
#%%create Obstacle objects:
    
if '6' in path_directory:
    sphered_rocks = []
    obj_type = 'Sphered_Rock'
    path_data = np.loadtxt(path_directory + obj_type + '.txt', delimiter = ',')
    cloud_data = np.loadtxt(path_directory + 'Sphere_Data' + '.txt', delimiter = ',')
    cloud_positions = cloud_data[:,0:3]
    cloud_rads = cloud_data[:,-1]
#    num_cols = int(path_data.shape[1])
    num_cols = 1
    for obstacle_index in range(0, num_cols, 6):
        path_loc = []
        path_dir = []
        loc_slice = slice(obstacle_index, obstacle_index+3)
        dir_slice = slice(obstacle_index+3, obstacle_index+6)
        path_loc = path_data[:,loc_slice]
        path_dir = path_data[:,dir_slice]
        sphered_rocks.append(Sphered_Rock(path_loc, path_dir,
                                          cloud_positions, cloud_rads))
        
#if '7' in path_directory:
#    obstacles = []
#    obj_type = 'Obstacle'
#    path_data = np.loadtxt(path_directory + obj_type + '.txt', delimiter = ',')
#    
#    num_cols = int(path_data.shape[1])
#    for obstacle_index in range(0, num_cols, 6):
#        path_loc = []
#        path_dir = []
#        loc_slice = slice(obstacle_index, obstacle_index+3)
#        dir_slice = slice(obstacle_index+3, obstacle_index+6)
#        path_loc = path_data[:,loc_slice]
#        path_dir = path_data[:,dir_slice]
#        obstacles.append(Obstacle(path_loc, path_dir))
#        
#%%draw system:
#load time data:
total_time = np.loadtxt(path_directory + 'Time_Data.txt', delimiter = ',')

try:
    sphered_rocks
except NameError:
    sphered_rocks = None
    
#draw_system(chassis, road_wheels, sprockets, idlers, track_units, obstacles, total_time = total_time, path_directory = path_directory)
draw_system(chassis, road_wheels, sprockets, idlers, track_units, 
            path_directory = path_directory, total_time = total_time, sphered_rocks = sphered_rocks)