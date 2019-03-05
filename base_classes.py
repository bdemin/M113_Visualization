import numpy as np
import vtk

from get_surface_actor import get_surface_actor
from set_actor_visuals import set_actor_visuals
from get_3dsurface_actor import get_3dsurface_actor
from place_object import place_object


def find_angle(x0, y0):
    return np.arctan(y0/x0)*180/np.pi+90

def get_stl_actor(filename):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    return actor

        
directory = 'STL/'
class Chassis(object):
    def __init__(self, path_loc, path_dir):        
        self.position = path_loc[0]
        self.angles = path_dir[0]
        self.type = 'Chassis'
        self.path = self.Path(path_loc, path_dir)
        self.actor = get_stl_actor(directory + self.type + '.STL')
        set_actor_visuals(self.actor, self.type)
        self.actor.GetProperty().SetInterpolationToPhong()
        
    def Path(self, path_loc, path_dir):
        self.path_loc = path_loc
        self.path_dir = path_dir
        
    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles
        
    def __repr__(self):
        return "%r\n location: %r \n orientation: %r" % (self.type,
                                                           self.position,
                                                           str(np.rad2deg(self.angles)))


class Road_Wheel(object):
    def __init__(self, side, path_loc, path_dir):
        self.position = path_loc[0]
        self.angles = path_dir[0]
        self.side = side
        self.type = 'Road_Wheel'
        self.path = self.Path(path_loc, path_dir)
        self.actor = get_stl_actor(directory + self.type + '.STL')
        set_actor_visuals(self.actor, self.type)        
        
    def Path(self, path_loc, path_dir):
        self.path_loc = path_loc
        self.path_dir = path_dir
        
        
    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles

    def __repr__(self):
        return "%r\n location: %r \n orientation: %r" % (self.type,
                                                           self.position,
                                                           str(np.rad2deg(self.angles)))

class Sprocket(object):
    def __init__(self, side, path_loc, path_dir):
        self.position = path_loc[0]
        self.angles = path_dir[0]
        self.side = side
        self.type = 'Sprocket'
        self.path = self.Path(path_loc, path_dir)
        self.actor = get_stl_actor(directory + self.type + '.STL')
        set_actor_visuals(self.actor, self.type)
        
        
    def Path(self, path_loc, path_dir):
        self.path_loc = path_loc
        self.path_dir = path_dir
        
        
    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles

    def __repr__(self):
        return "%r\n location: %r \n orientation: %r" % (self.type,
                                                           self.position,
                                                           str(np.rad2deg(self.angles)))
        
class Idler(object):
    def __init__(self, side, path_loc, path_dir):
        self.position = path_loc[0]
        self.angles = path_dir[0]
        self.side = side
        self.type = 'Idler'
        self.path = self.Path(path_loc, path_dir)
        self.actor = get_stl_actor(directory + self.type + '.STL')
        set_actor_visuals(self.actor, self.type)
        
        
    def Path(self, path_loc, path_dir):
        self.path_loc = path_loc
        self.path_dir = path_dir
        
        
    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles
        
    def __repr__(self):
        return "%r\n location: %r \n orientation: %r" % (self.type,
                                                           self.position,
                                                           str(np.rad2deg(self.angles)))
        
        
class Track_Unit(object):
    def __init__(self, path_loc, path_dir):
        self.position = path_loc[0]
        self.angles = path_dir[0]
        self.type = 'Track_Unit'
        self.path = self.Path(path_loc, path_dir)
        self.actor = get_stl_actor(directory + self.type + '.STL')
        set_actor_visuals(self.actor, self.type)
        
        
    def Path(self, path_loc, path_dir):
        self.path_loc = path_loc
        self.path_dir = path_dir
        
        
    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles
        
    def __repr__(self):
        return "%r\n location: %r \n orientation: %r" % (self.type,
                                                           self.position,
                                                           str(np.rad2deg(self.angles)))
    
class Surface(object):
    def __init__(self, path_directory):
        self.type = 'Surface'
        resolution = 6
        
        if '3' in path_directory:
            width = 2
            left_offset = width/2
            right_offset = -width/2
            file = 'Ground_Left.txt'
            left_actor = get_surface_actor(width, resolution, left_offset, path_directory + file)
            file = 'Ground_Right.txt'
            right_actor = get_surface_actor(width, resolution, right_offset, path_directory + file)
            self.actors = [left_actor, right_actor]
            
        elif '4' in path_directory:
            self.actors = [get_3dsurface_actor(path_directory)]
        elif '5' in path_directory:
            self.actors = [get_3dsurface_actor(path_directory)]
        else:
            width = 10
            offset = 0
            file = 'Ground_Rock2D.txt'
            self.actors = [get_surface_actor(width, resolution, offset, path_directory + file)]
            
            
class Obstacle():
    def __init__(self, path_loc, path_dir):
        self.type = 'Obstacle'
        self.position = path_loc[0]
        self.angles = path_dir[0]
        self.path_loc = path_loc
        self.path_dir = path_dir
        self.actor = get_stl_actor(directory + self.type + '.STL')
#        set_actor_visuals(self.actor, self.type)
#        self.actor.GetProperty().SetInterpolationToPhong()

        
    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles
        
    def __repr__(self):
        return "%r\n location: %r \n orientation: %r" % (self.type,
                                                           self.position,
                                                           str(np.rad2deg(self.angles)))
        

class Sphered_Rock():
    def __init__(self, path_loc, path_dir, cloud, rads):
        self.position = path_loc[0]
        self.direction = path_dir[0]
        self.path_loc = path_loc
        self.path_dir = path_dir
        self.cloud = cloud
        self.actors = self.Get_Rock(self.cloud + self.position, rads)
        
#        self.actor = get_stl_actor(directory + self.type + '.STL')
        
    def Get_Sphere(self, position, radius):
        source = vtk.vtkSphereSource()
        source.SetCenter(position)
        source.SetRadius(radius)
        source.SetThetaResolution(3)
        source.SetPhiResolution(3)
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.3,0.3,0.3)
        return actor
    
    def Get_Rock(self, positions, rads):
        rock_actors = []
        for i in range(positions.shape[0]):
            actor = self.Get_Sphere(positions[i,:], rads[i])
            rock_actors.append(actor)            
        return rock_actors
        
    def Move(self, new_position, new_direction):
        self.position = new_position
        self.direction = new_direction
            
    def Update_Spheres(self):
        for i, pos in enumerate(self.cloud):
            place_object(self.actors[i], pos + self.position, self.direction)