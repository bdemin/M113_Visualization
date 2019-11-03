import numpy as np
from vtk import vtkTransform, vtkTransformPolyDataFilter

from graphics.helpers import get_stl_actor, set_actor_visuals


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

        if self.side:
            return Asymmetrical()
        else:
            return Symmetrical()

    def __repr__(self):
        return "%r at: %r, %r" % (self.type,
                                    str(self.position),
                                    str(np.rad2deg(self.angles)))

    def Move(self, new_position, new_angles):
        self.position = new_position
        self.angles = new_angles



class Symmetrical(Body):
    def __init__(self):
        pass

    def place_object(self):
        print('sym')
        # Can remove this
        trans = vtkTransform()
        trans.PreMultiply()

        trans.Translate(*self.position)

        trans.RotateZ(np.rad2deg(self.angles[2]))
        trans.RotateY(np.rad2deg(self.angles[1]))
        trans.RotateX(np.rad2deg(self.angles[0]))

        self.actor.SetUserTransform(trans)

class Asymmetrical(Body):
    def __init__(self):
        pass

    def place_object(self):
        print('asym')
        if self.side == 'L':
            first_angles = (chassis_angles[0], chassis_angles[1], chassis_angles[2]-np.pi)
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