from bodies.helpers import create_bodies


class Vehicle(object):
    def __init__(self, path):
        self.bodies = dict()
        self.bodies['Chassis'] = create_bodies(path, 'Chassis')

        
    
class M113(Vehicle):
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
