import numpy as np

from bodies.classes import Body

class Vehicle(object):
    # Metaclass to define common attributes of DBD vehicles.
    
    def __init__(self, path):
        self.data = dict()
        self.data['chassis'] = create_bodies(path, 'Chassis')
        # can be improved (inputs, func rather than method, path, etc)

    def update(self, timer_count):
        chassis_angles = self.data['chassis'][0].angles
        for bodies in self.data.values():
            for body in bodies:
                body.update(timer_count)
                body.place(chassis_angles)


class M113(Vehicle):
    # Inherits from Vehicle and adds all the relevant attributes for visualizing M113 DBD results.
    
    def __init__(self, path):
        Vehicle.__init__(self, path)
        self.data['road_wheels'] = create_bodies(path, 'Road_Wheel', side = True)
        self.data['trailing_arms'] = create_bodies(path, 'Trailing_Arm', side = True)
        self.data['sprockets'] = create_bodies(path, 'Sprocket', side = True)
        self.data['idlers'] = create_bodies(path, 'Idler', side = True)
        self.data['track_units'] = create_bodies(path, 'Track_Unit', side = True)


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
    # Return a list of specific bodies data

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
        bodies.append(Body.factory(type_, path_loc, path_dir, side))
    return bodies
