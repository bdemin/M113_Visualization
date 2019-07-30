import numpy as np

from graphics.helpers import get_stl_actor, set_actor_visuals
from graphics.get_surface_actor import get_surface_actor
from graphics.get_3dsurface_actor import get_3dsurface_actor
from graphics.place_object import place_object


directory = 'graphics/STL_data/'
class Body(object):
    def __init__(self, type_, path_loc, path_dir, side = None):
        self.type = type_

        self.path_loc = path_loc
        self.path_dir = path_dir

        self.position = path_loc[0]
        self.angles = path_dir[0]
        if side:
            self.side = side

        self.actor = get_stl_actor(directory + self.type + '.STL')
        set_actor_visuals(self.actor, self.type)
        self.actor.GetProperty().SetInterpolationToPhong()

    def __repr__(self): 
        return "%r\n location: %r \n orientation: %r" % (self.type,
                                                           self.position,
                                                           str(np.rad2deg(self.angles)))

    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles


class Surface(object):
    def __init__(self, path_directory):
        self.type = 'Surface'
        resolution = 6
        
        if 'Simulation_3' in path_directory:
            width = 2
            left_offset = width/2
            right_offset = -width/2
            file = 'Ground_Left.txt'
            left_actor = get_surface_actor(width, resolution, left_offset, path_directory + file)
            file = 'Ground_Right.txt'
            right_actor = get_surface_actor(width, resolution, right_offset, path_directory + file)
            self.actors = [left_actor, right_actor]
            
        elif 'Simulation_4' in path_directory:
            self.actors = [get_3dsurface_actor(path_directory)]
        elif '3d_Rocks1' in path_directory:
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
        
        
    def Get_Sphere(self, position, radius):
        source = vtkSphereSource()
        source.SetCenter(position)
        source.SetRadius(radius)
        source.SetThetaResolution(3)
        source.SetPhiResolution(3)
        
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        
        actor = vtkActor()
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