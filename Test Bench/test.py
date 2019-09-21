import numpy as np
import vtk


def get_stl_actor(filename):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    return actor


directory = 'graphics/STL_data/'
class Body(object):
    def __init__(self, type_, position, angles, side = None):
        self.type = type_

        self.position = position
        self.angles = angles

        self.side = side

        self.actor = get_stl_actor(directory + self.type + '.STL')
        self.trans = vtk.vtkTransform()
        self.trans.PostMultiply()
        

def trans_matrix(dx, dy, dz):
    matrix = np.eye(4)
    matrix[0,3] = dx
    matrix[1,3] = dy
    matrix[2,3] = dz
    return matrix

def rot_matrix(x, y, z):
    sin = np.sin
    cos = np.cos
    matrix = []

    Cx = cos(x)
    Cy = cos(y)
    Cz = cos(z)

    Sx = sin(x)
    Sy = sin(y)
    Sz = sin(z)

    matrix.append(Cy * Cz)
    matrix.append(Cz * Sx * Sy-Cx * Sz)
    matrix.append(Sx * Sz+Cx * Cz * Sy)
    matrix.append(0)
    
    matrix.append(Cy * Sz)
    matrix.append(Cx * Cz+Sx * Sy * Sz)
    matrix.append(Cx * Sy * Sz-Cz * Sx)
    matrix.append(0)
    
    matrix.append(-Sy)
    matrix.append(Cy * Sx)
    matrix.append(Cx * Cy)
    matrix.append(0)
    
    matrix.append(0)
    matrix.append(0)
    matrix.append(0)
    matrix.append(1)
    
    matrix = np.asarray(matrix).reshape(4,4)
    return matrix


def create_bodies(directory, type_, side = None):
    bodies = []
    path_data = np.loadtxt(directory + type_ + '.txt', delimiter = ',')
    num_cols = path_data.shape[0]
    for index in range(0, num_cols, 6):
        if side:
            if index < num_cols/2:
                side = 'L'
            else:
                side = 'R'

        position = path_data[index+0:index+3]
        angles = path_data[index+3:index+6]
        bodies.append(Body(type_, position, angles, side))  
    return bodies



class vtkTimerCallback(object):
    def __init__(self, renderer, renWin, data):
        self.time = 1
        self.renderer = renderer
        self.camera = self.renderer.GetActiveCamera()
        self.camera.SetViewUp(0,1,1)
        for body_type in data:
            for body in body_type:
                self.renderer.AddActor(body.actor)


    def execute(self, obj, event):
        for body_type in self.data:
            for body in body_type:
                rot_mat = rot_matrix(*body.angles)
                trans = vtk.vtkTransform()
                vtk_matrix = vtk.vtkMatrix4x4()


                    # rotations_matrix = np.matmul(rot_matrix(*(first_angles[0],0,first_angles[2])), rot_matrix(*y_rotation))

                    # final_matrix = np.matmul(trans_matrix(*new_pos), rotations_matrix)
                    
                m, n = rot_mat.shape
                for i in range(m):
                    for j in range(n):
                        vtk_matrix.SetElement(i, j, rot_mat[i][j])
                trans.SetMatrix(vtk_matrix)
                # transformFilter = vtk.vtkTransformPolyDataFilter()
                # transformFilter.SetTransform(trans)
                body.actor.SetUserTransform(trans)
                # body.trans.Identity()
                # body.trans.Translate(body.position)
                # body.trans.RotateX(np.rad2deg(body.angles[0]))
                # body.trans.RotateY(np.rad2deg(body.angles[1]))
                # body.trans.RotateZ(np.rad2deg(body.angles[2]))
                # body.trans.RotateWXYZ(np.rad2deg(body.angles[0]), 1, 0, 0)
                # body.trans.RotateWXYZ(np.rad2deg(body.angles[1]), 0, 1, 0)
                # body.trans.RotateWXYZ(np.rad2deg(body.angles[2]), 0, 0, 1)
                # body.actor.SetUserTransform(body.trans)
        # print(body.angles,'\n')
        obj.GetRenderWindow().Render()


    def keypress(self, obj, event):
        key = obj.GetKeySym()

        if key == 'c':
            for body_type in self.data:
                for body in body_type:
                    body.position[0] += 0.5
        
        if key == 'v':
            for body_type in self.data:
                for body in body_type:
                    body.position[0] -= 0.5

        if key == 'x':
            for body_type in self.data:
                for body in body_type:
                    body.angles[0] += 0.1
                    if body.angles[0] > 2*np.pi:
                        body.angles[0] -= 2*np.pi

        if key == 'y':
            for body_type in self.data:
                for body in body_type:
                    body.angles[1] += 0.1
                    if body.angles[1] > 2*np.pi:
                        body.angles[1] -= 2*np.pi

        if key == 'z':
            for body_type in self.data:
                for body in body_type:
                    body.angles[2] += 0.1
                    if body.angles[2] > 2*np.pi:
                        body.angles[2] -= 2*np.pi


def get_actors():
    from os import listdir

    actors = []
    stl_files_list = listdir('graphics/STL_data')

    for stl_file in stl_files_list:
        actor = get_stl_actor(stl_file)
        actors.append(actor)

    return actors


def main():
    renderer = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    axesActor = vtk.vtkAxesActor()
    trans = vtk.vtkTransform()
    trans.Identity()
    axesActor.SetUserTransform(trans)
    # trans.Scale(4, 4, 4)
    widget = vtk.vtkOrientationMarkerWidget()
    widget.SetOrientationMarker(axesActor)
    widget.SetInteractor(iren)
    widget.SetEnabled(1)
    widget.InteractiveOff()
    renderer.AddActor(axesActor)

    directory = 'Test Bench/'
    chassis = create_bodies(directory, 'Chassis')
    road_wheels = create_bodies(directory, 'Road_Wheel', side = True)
    trailing_arms = create_bodies(directory, 'Trailing_Arm', side = True)
    sprockets = create_bodies(directory, 'Sprocket', side = True)
    idlers = create_bodies(directory, 'Idler', side = True)
    track_units = create_bodies(directory, 'Track_Unit')

    # data = [chassis, road_wheels, trailing_arms, sprockets, idlers, track_units]
    data = [chassis]

    # trans = vtk.vtkTransform()
    # trans.Identity()
    # actor.SetUserTransform(trans)

    renderer.GradientBackgroundOn()
    renderer.SetBackground(0,0,0.5)
    renderer.SetBackground2(0.2,0.2,0.6)
    renWin.SetSize(1600, 960)

    iren.Initialize()

    callback = vtkTimerCallback(renderer, renWin, data)
    callback.data = data
    iren.AddObserver('TimerEvent', callback.execute)
    iren.AddObserver('KeyPressEvent', callback.keypress)

    iren.CreateRepeatingTimer(50)
    iren.Start()

if __name__ == '__main__':
    main()
