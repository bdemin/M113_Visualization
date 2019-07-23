import numpy as np
from vtk import vtkSTLReader, vtkPolyDataMapper, vtkActor, vtkSphereSource

        
directory = 'STL/'
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