import numpy as np

from vtk import vtkSTLReader, vtkPolyDataMapper, vtkActor, vtkTransform


class Vehicle(object):
    # Class for containing common attributes.
    
    def __init__(self, path, vehicle_type):
        self.vehicle_type = vehicle_type
        self.data = dict()
        self.data['chassis'] = create_bodies(path, vehicle_type, 'Chassis')
        # can be improved (inputs, func rather than method, path, etc)

    def update(self, timer_count):
        chassis_angles = self.data['chassis'][0].angles
        for bodies in self.data.values():
            for body in bodies:
                body.update(timer_count)
                body.place(chassis_angles)


class M113(Vehicle):
    # Container for all the relevant bodies of an M113 vehicle
    
    def __init__(self, path):
        vehicle_type = self.__class__.__name__
        Vehicle.__init__(self, path, vehicle_type)
        self.data['road_wheels'] = create_bodies(path, vehicle_type, 'Road_Wheel', side = True)
        self.data['trailing_arms'] = create_bodies(path, vehicle_type, 'Trailing_Arm', side = True)
        self.data['sprockets'] = create_bodies(path, vehicle_type, 'Sprocket', side = True)
        self.data['idlers'] = create_bodies(path, vehicle_type, 'Idler', side = True)
        self.data['track_units'] = create_bodies(path, vehicle_type, 'Track_Unit', side = True)


class Eitan(Vehicle):
    def __init__(self, path):
        vehicle_type = self.__class__.__name__
        Vehicle.__init__(self, path, vehicle_type)
        self.data['road_wheels'] = create_bodies(path, vehicle_type, 'Road_Wheel', side = True)


class MK4(Vehicle):
    def __init__(self, path):
        Vehicle.__init__(self, path)


class D9(Vehicle):
    def __init__(self, path):
        Vehicle.__init__(self, path)
        

def create_bodies(path_directory, vehicle_type, type_, side = None):
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
        bodies.append(Body.factory(type_, path_loc, path_dir, vehicle_type, side))
    return bodies


class Body(object):
    # Class factory to define a general body object

    def __init__(self, type_, path_loc, path_dir, vehicle_type, side = None):
        self.type = type_

        self.path_loc = path_loc
        self.path_dir = path_dir

        self.position = path_loc[0]
        self.angles = path_dir[0]
        
        self.side = side
        
        directory = 'resources/STL_data/' + vehicle_type +'/' + self.type + '.STL'
        self.actor = self.get_stl_actor(directory)
        self.actor.GetProperty().SetInterpolationToPhong()

        self.set_actor_visuals(self.actor, self.type)

    def __repr__(self):
        return "%r at: %r, %r" % (self.type,
                                    str(self.position),
                                    str(np.rad2deg(self.angles)))

    @staticmethod
    def factory(type_, path_loc, path_dir, vehicle_type, side = None):
        if side:
            return Asymmetrical(type_, path_loc, path_dir, vehicle_type, side)
        return Symmetrical(type_, path_loc, path_dir, vehicle_type)

    def update(self, timer_count):
        self.position = self.path_loc[timer_count]
        self.angles = self.path_dir[timer_count]

    def get_stl_actor(self, filename):
        reader = vtkSTLReader()
        reader.SetFileName(filename)
        
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        
        actor = vtkActor()
        actor.SetMapper(mapper)
        
        return actor

    def set_actor_visuals(self, actor, _type):
        # Class level definition of visual properties

        Chassis = {'color':(0.244, 0.275, 0.075), 'ambi':0.1, 'ambic':(0.3,0.3,0.3), 'diff':0.9, 'diffc':(0.396, 0.263, 0.129), 'spec':0.6, 'specp':10}
        Road_Wheel = {'color':(0.194, 0.225, 0.025), 'ambi':0.4, 'ambic':(1,1,1), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
        Sprocket = {'color':(0.194, 0.225, 0.025), 'ambi':0.3, 'ambic':(0,0,0), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
        Idler = {'color':(0.194, 0.225, 0.025), 'ambi':0.3, 'ambic':(0,0,0), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
        Track_Unit = {'color':(0.35,0.35,0.35), 'ambi':0.3, 'ambic':(0,0,0), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
        Trailing_Arm = {'color':(0.35,0.35,0.35), 'ambi':0.3, 'ambic':(0,0,0), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
        _type = vars()[_type]
        
        actor.GetProperty().SetColor(_type['color'])
        actor.GetProperty().SetAmbient(_type['ambi'])
    #    actor.GetProperty().SetAmbientColor(_type['ambic'])
        actor.GetProperty().SetDiffuse(_type['diff'])
    #    actor.GetProperty().ShadingOff()
    #    actor.GetProperty().LightingOff()
    #    actor.GetProperty().SetDiffuseColor(_type['diffc'])
        actor.GetProperty().SetSpecular(_type['spec'])
        actor.GetProperty().SetSpecularPower(_type['specp'])


class Symmetrical(Body):
    # Class definition for bodies which are symmetrical

    def __init__(self, type_, path_loc, path_dir, vehicle_type):
        Body.__init__(self, type_, path_loc, path_dir, vehicle_type) #remove side

    def place(self, chassis_angles):
        # Can remove this?
        trans = vtkTransform()
        trans.PreMultiply()

        trans.Translate(*self.position)

        trans.RotateZ(np.rad2deg(self.angles[2]))
        trans.RotateY(np.rad2deg(self.angles[1]))
        trans.RotateX(np.rad2deg(self.angles[0]))

        self.actor.SetUserTransform(trans)

class Asymmetrical(Body):
    # Class definition for bodies which are asymmetrical

    def __init__(self, type_, path_loc, path_dir, vehicle_type, side = None):
        Body.__init__(self, type_, path_loc, path_dir, vehicle_type, side)

    def place(self, chassis_angles):
        if self.side == 'L':
            first_angles = (chassis_angles[0], chassis_angles[1], chassis_angles[2] - np.pi)
            y_rotation = -self.angles[1]
        elif self.side == 'R':
            first_angles = chassis_angles[:]
            y_rotation = self.angles[1]
        
        trans = vtkTransform()
        trans.PreMultiply()
        trans.Translate(*self.position)
        
        trans.RotateX(np.rad2deg(first_angles[0]))
        trans.RotateY(np.rad2deg(first_angles[1]))
        trans.RotateZ(np.rad2deg(first_angles[2]))
        
        trans.RotateY(np.rad2deg(y_rotation))

        self.actor.SetUserTransform(trans)
