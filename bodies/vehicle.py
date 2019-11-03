import numpy as np


class Vehicle(object):
    # Metaclass to define common attributes of DBD vehicles.
    def __init__(self, path):
        self.bodies = dict()
        self.bodies['Chassis'] = create_bodies(path, 'Chassis')


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
        Vehicle.__init__(self, path)


class MK4(Vehicle):
    def __init__(self):
        Vehicle.__init__(self, path)


class D9(Vehicle):
    def __init__(self):
        Vehicle.__init__(self, path)
        