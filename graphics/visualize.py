import numpy as np
from vtk import vtkCamera, vtkRenderer, vtkRenderWindow, \
    vtkRenderWindowInteractor, vtkAxesActor, \
    vtkOrientationMarkerWidget

from graphics.place_camera import place_camera
from graphics.place_object import place_all_bodies
from graphics.transformations import scale_actor
from graphics.draw_text import draw_text

from help_functions.event_handling import keyboard_events

from bodies.classes import Surface

from graphics.get_video import get_video, get_snapshots, snap


record = False
# record = True
class vtkTimerCallback(object):
    def __init__(self, renderer, renWin, rate):
#        I can try putting most visualize commands here?
        self.timer_count = 1
        self.rate = rate
        self.pause = True
        self.camera_flag = True
        
        self.renderer = renderer
        self.camera = vtkCamera()
        self.renderer.SetActiveCamera(self.camera)
        
        self.text_actor = draw_text('Init')
        self.renderer.AddActor(self.text_actor)
        
        if record:
            self.video_count = 1
            self._filter, self.writer = get_video(renWin, self.rate, 'M113_' + str(self.video_count))

    def execute(self, obj, event):
        self.pause, self.camera_flag = keyboard_events(obj, self.pause, self.camera_flag)
        print(self.pause, self.camera_flag)

        if self.camera_flag:
            place_camera(self.camera, self.data[0][0].path_loc[self.timer_count], self.data[0][0].path_dir[self.timer_count])

        place_all_bodies(self.data, self.timer_count)

        if self.sphered_rocks != None:                    
            for sphered_rock in self.sphered_rocks:
                sphered_rock.Move(sphered_rock.path_loc[self.timer_count],
                                    _object.path_dir[self.timer_count])
                sphered_rock.Update_Spheres()
                
        if 0 <= self.timer_count and self.timer_count < int(self.num_frames - 1):
            obj.GetRenderWindow().Render()
            if record:
                if self.timer_count % 500 == 0:
                    self.writer.End()
                    self.video_count += 1
                    self._filter, self.writer = get_video(self.iren.GetRenderWindow(), self.rate, 'M113_' + str(self.video_count))
                self._filter.Modified()
                self.writer.Write()
            if self.pause == True:
                self.text_actor.SetInput('Pause')
                obj.GetRenderWindow().Render()
            else:
                text = 'time = %.1fs' % (self.timer_count * self.dt)
                self.text_actor.SetInput(text)
                self.timer_count += 1
        else:
            if record:
                self.writer.End()
            self.timer_count = 0
            self.iren.DestroyTimer()
            self.iren.GetRenderWindow().Finalize()
            self.iren.TerminateApp()
            print('Simulation End')


def visualize(*args, path_directory, total_time = 25, sphered_rocks = None):
    # create renderer, figure and axes:
    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # add stationary axes:    
    axesActor = vtkAxesActor()
    scale_actor(axesActor, 4)
    # renderer.AddActor(axesActor)
    widget = vtkOrientationMarkerWidget()
    widget.SetOrientationMarker(axesActor)
    widget.SetInteractor(iren)
    widget.SetEnabled(1)
    widget.InteractiveOff()
    
    renderer.GradientBackgroundOn()
    renderer.SetBackground(0,0,0.5)
    renderer.SetBackground2(0.2,0.2,0.6)
    renWin.SetSize(1920, 1080)

    # add all actors to the renderer
    for i in range(len(args)):
        for obj in args[i]:
            renderer.AddActor(obj.actor)

    surface = Surface(path_directory)
    for actor in surface.actors:
        renderer.AddActor(actor)
        
    if sphered_rocks is not None:
        for sphered_rock in sphered_rocks:
            for i, sphere_actor in enumerate(sphered_rock.actors):
                renderer.AddActor(sphere_actor)
                place_object(actor, sphered_rock.position + sphered_rock.cloud[i], sphered_rock.direction)
                
    iren.Initialize()

    # Sign up to receive TimerEvent
    num_frames = args[0][0].path_dir.shape[0]
    FPS = num_frames/total_time
    FPMS = FPS/1000
    
    callback = vtkTimerCallback(renderer, renWin, FPS)
    callback.data = args
    callback.ren = renderer
    callback.num_frames = args[0][0].path_dir.shape[0]
    callback.iren = iren
    callback.dt = total_time/callback.num_frames
    callback.sphered_rocks = sphered_rocks
    
    iren.AddObserver('TimerEvent', callback.execute)
    
    iren.CreateRepeatingTimer(int(1/FPMS)) #ms
    iren.Start()