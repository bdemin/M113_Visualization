import numpy as np

from bodies.helpers import create_bodies
from graphics.visualize import visualize

from helpers.functions import get_directory
from simulation_description import show_description


path = '../Eitan_Model/Data_Movies/'
directory = get_directory(path)

show_description(directory)

#%% Create bodies
chassis = create_bodies(directory, 'Chassis')
wheels = create_bodies(directory, 'Wheel', side = True)
upper_control_arms = create_bodies(directory, 'Upper_Control_Arm', side = True)
lower_control_arms = create_bodies(directory, 'Lower_Control_Arm', side = True)
wheel_carriers1 = create_bodies(directory, 'Wheel_Carrier_L')
wheel_carriers2 = create_bodies(directory, 'Wheel_Carrier_R')
wheel_carriers = wheel_carriers1 + wheel_carriers2

# Test trailing arm
# offset = 0.1
# for arm in trailing_arms:
#     if arm.side == 'L':
#         arm.path_loc[:,1] += offset
#     else:
#         arm.path_loc[:,1] -= offset

#%% Visualize
# Load time data
# total_time = np.loadtxt(directory + 'Time_Data.txt', delimiter = ',')
total_time = 30

# Visualize all bodies
visualize(chassis, wheels, upper_control_arms, lower_control_arms, wheel_carriers,
            directory = directory, total_time = total_time)

# Visualize specific bodies
# visualize(chassis, total_time = total_time, directory = directory)
