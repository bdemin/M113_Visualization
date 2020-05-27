from vtk import vtkCamera


class Camera(vtkCamera):
    # Camera class for controlling various scene views

    def __init__(self, distance = 14, view = 'isometric'):
        super().__init__()
        self.current_view = view
        self.distance = distance
        self.slope = 0
        self.is_on = True
        
    def place_camera(self, frame, chassis_pos_and_dir):

        chassis_pos, chassis_dir = chassis_pos_and_dir

        if self.current_view == 'isometric':
            self.SetViewUp([0,0,1])
            self.roll_angle = 0
            
            dir_vec = np.array((-1,-1,1))
            dir_vec = dir_vec / np.linalg.norm(dir_vec)
            camera_pos = chassis_pos + self.distance*dir_vec
            cam_focal_point = chassis_pos
            

