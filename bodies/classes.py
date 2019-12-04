import numpy as np

# from vtk import vtkTransform

from graphics.helpers import get_stl_actor, set_actor_visuals
from graphics.get_surface_actor import get_surface_actor
from graphics.get_3dsurface_actor import get_3dsurface_actor


directory = 'graphics/STL_data/'
class Body(object):
    def __init__(self, type_, path_loc, path_dir, side = None):
        self.type = type_

        self.path_loc = path_loc
        self.path_dir = path_dir

        self.position = path_loc[0]
        self.angles = path_dir[0]
        self.side = side

        if type_ == 'Chassis':
            self.actor = get_stl_actor(directory + self.type + '_fix.STL')
            # self.actor = get_stl_actor(directory + self.type + '.STL')
        else:
            self.actor = get_stl_actor(directory + self.type + '.STL')
        set_actor_visuals(self.actor, self.type)
        self.actor.GetProperty().SetInterpolationToPhong()

        # self.trans = vtkTransform()
        # self.actor.SetUserTransform(self.trans)

    def __repr__(self):
        return "%r\n location: %r \n orientation: %r" % (self.type,
                                                           self.position,
                                                           str(np.rad2deg(self.angles)))

    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles


class Surface(object):
    def __init__(self, path_directory, chassis_cg = None):
        self.type = 'Surface'
        size_x = 301; size_y = 701
        ground_surf = -0.6 * np.ones((size_x, size_y))

        strings = ['Brake', 'OverSteering']
        if 'Slope' in path_directory:
            ground_surf[:,0] = np.arange(-20, -20 + size_x*0.2, 0.2)
            ground_surf[0,:] = np.arange(-23, -23 + size_y*0.2, 0.2)

        elif 'Step' in path_directory:
            ground_surf[:,0] = np.arange(-20, -20 + size_x*0.2, 0.2)
            ground_surf[0,:] = np.arange(-20, -20 + size_y*0.2, 0.2)
            
            step_x_loc = 7.1
            step_start_ind = np.abs(np.asarray(ground_surf[:,0]) - step_x_loc).argmin()
            step_end_ind = np.abs(np.asarray(ground_surf[:,0]) - 11).argmin()
            ground_surf[step_start_ind:, 1:] = 0
        
        elif any(x in path_directory for x in strings):
            ground_surf[:,0] = np.arange(-20, -20 + size_x*0.35, 0.35)
            ground_surf[0,:] = np.arange(-20, -20 + size_y*0.2, 0.2)

        elif 'Turning' in path_directory:
            # need to find slope?
            # ground_surf[:,0] = np.arange(-20, -20 + size_x*0.2, 0.2)
            step = 0.5
            ground_surf[:,0] = np.arange(-40, -40 + size_x*step, step)
            # ground_surf[0,:] = np.arange(-23, -23 + size_y*0.2, 0.2)
            ground_surf[0,:] = np.arange(-40, -40 + size_y*step, step)

        surface_w = 150
        ground_surf = (ground_surf[:,0], ground_surf[0,51:surface_w], ground_surf[1:,51:surface_w])
        self.actors = get_3dsurface_actor(path_directory, ground_surf, chassis_cg)[0:2]
