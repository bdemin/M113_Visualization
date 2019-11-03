import numpy as np

from bodies.classes import Body

class Vehicle(object):
    # Metaclass to define common attributes of DBD vehicles.
    
    def __init__(self, path):
        self.bodies = dict()
        self.bodies['Chassis'] = create_bodies(path, 'Chassis')
        # can be improved (inputs, func rather than method, path, etc)


class M113(Vehicle):
    # Inherits from Vehicle and adds all the relevant attributes for visualizing M113 DBD results.
    
    def __init__(self, path):
        Vehicle.__init__(self, path)
        self.bodies['road_wheels'] = create_bodies(path, 'Road_Wheel', side = True)
        self.bodies['trailing_arms'] = create_bodies(path, 'Trailing_Arm', side = True)
        self.bodies['sprockets'] = create_bodies(path, 'Sprocket', side = True)
        self.bodies['idlers'] = create_bodies(path, 'Idler', side = True)
        self.bodies['track_units'] = create_bodies(path, 'Track_Unit')


class Eitan(Vehicle):
    def __init__(self):
        Vehicle.__init__(self)


class MK4(Vehicle):
    def __init__(self):
        Vehicle.__init__(self)


class D9(Vehicle):
    def __init__(self):
        Vehicle.__init__(self)
        

def create_bodies(path_directory, type_, side = None):
    # Return list of similar bodies

    bodies = []
    path_data = np.loadtxt(path_directory + type_ + '.txt', delimiter = ',')
    num_cols = int(path_data.shape[1])
    for index in range(0, num_cols, 6):
        loc_slice = slice(index, index+3)
        dir_slice = slice(index+3, index+6)
        path_loc = np.copy(path_data[:, loc_slice])
        path_dir = np.copy(path_data[:, dir_slice])
        if side:
            if index < num_cols/2:
                side = 'L'
                path_dir[:,2] = path_dir[:,2] - np.pi
                path_dir[:,0] = -path_dir[:,0]
            else:
                side = 'R'
        bodies.append(Body(type_, path_loc, path_dir, side))
    return bodies