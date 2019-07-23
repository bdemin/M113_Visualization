import numpy as np

from bodies.helpers import create_bodies
from graphics.visualize import visualize

from base_classes import Sphered_Rock
from simulation_description import show_description


path_directory = '../M113_tests/Data_Movies/3d_Rocks1/'
# path_directory = '../M113_PY/save_data/data/'
show_description(path_directory)

#%%create 
chassis = create_bodies(path_directory, 'Chassis')
road_wheels = create_bodies(path_directory, 'Road_Wheel', side = True)
trailing_arms = create_bodies(path_directory, 'Trailing_Arm', side = True)
sprockets = create_bodies(path_directory, 'Sprocket', side = True)
idlers = create_bodies(path_directory, 'Idler', side = True)
track_units = create_bodies(path_directory, 'Track_Unit')

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
        
        
#%%visualize:
#load time data:
total_time = np.loadtxt(path_directory + 'Time_Data.txt', delimiter = ',')

try:
    sphered_rocks
except NameError:
    sphered_rocks = None
    
# visualize(chassis, road_wheels, sprockets, idlers, track_units, obstacles, total_time = total_time, path_directory = path_directory)
# visualize(chassis, road_wheels, trailing_arms, sprockets, idlers, track_units, 
            # path_directory = path_directory, total_time = total_time, sphered_rocks = sphered_rocks)
visualize(road_wheels, sprockets, idlers, 
            path_directory = path_directory, total_time = total_time, sphered_rocks = sphered_rocks)