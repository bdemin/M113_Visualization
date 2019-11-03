import numpy as np
import quaternion
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
        # self.trans.PostMultiply()
        self.actor.SetUserTransform(self.trans)
        

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

        cam_distance = (6, 6, 6)
        self.camera = vtk.vtkCamera()
        self.renderer.SetActiveCamera(self.camera)
        self.camera.SetViewUp(0,0,1)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetPosition(cam_distance)


        for body_type in data:
            for body in body_type:
                self.renderer.AddActor(body.actor)


    def execute(self, obj, event):
        for body_type in self.data:
            for body in body_type:
                body.trans.Identity()

                # Quaternion stuff
                yaw = body.angles[2]
                pitch = body.angles[1]
                roll = body.angles[0]

                cy = np.cos(yaw * 0.5)
                sy = np.sin(yaw * 0.5)
                cp = np.cos(pitch * 0.5)
                sp = np.sin(pitch * 0.5)
                cr = np.cos(roll * 0.5)
                sr = np.sin(roll * 0.5)

                w = cy * cp * cr + sy * sp * sr
                x = cy * cp * sr - sy * sp * cr
                y = sy * cp * sr + cy * sp * cr
                z = sy * cp * cr - cy * sp * sr

                body_quaternion = np.quaternion(w, x, y, z)

                # Convert to 4x4 vtkMatrix
                vtkmath = vtk.vtkMath()
                rot_mat_3x3 = np.zeros((3,3))
                vtkmath.QuaternionToMatrix3x3(body_quaternion.components, rot_mat_3x3)
                rot_mat_4x4 = np.zeros((4,4))
                rot_mat_4x4[0:3,0:3] = rot_mat_3x3[:,:]
                rot_mat_4x4[-1,-1] = 1
                
                vtk_matrix = vtk.vtkMatrix4x4()
                m, n = rot_mat_4x4.shape
                for i in range(m):
                    for j in range(n):
                        vtk_matrix.SetElement(i,j, rot_mat_4x4[i][j])

                body.trans.SetMatrix(vtk_matrix)
                body.actor.SetUserTransform(body.trans)

        print(body.angles,'\n')
        obj.GetRenderWindow().Render()


    def keypress(self, obj, event):
        key = obj.GetKeySym()


        if key == 'v':
            for body_type in self.data:
                for body in body_type:
                    body.angles[:] = 0


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
    data = [create_bodies(directory, 'Chassis')]

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
