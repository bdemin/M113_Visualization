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
        self.actors = [get_3dsurface_actor(path_directory)[0]]
