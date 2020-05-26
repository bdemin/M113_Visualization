from vtk import vtkCamera


class Camera(vtkCamera):
    # Camera class for controlling various scene views

    def __init__(self, distance = 14, view = 'isometric'):
        super().__init__()
        self.current_view = view
        self.distance = distance
        self.slope = 0
        self.is_on = True

