import numpy as np
from ctypes import windll

from vtk import vtkCamera, vtkRenderer, vtkRenderWindow, \
    vtkRenderWindowInteractor, vtkAxesActor, \
    vtkOrientationMarkerWidget, vtkTransform

from graphics.place_camera import place_camera
from graphics.place_object import place_all_bodies
from graphics.draw_text import draw_text
from graphics.get_video import get_video, get_snapshots, snap

from helpers.event_handling import keyboard_events

from bodies.classes import Surface


record_video_bool = True
record_video_bool = False

class vtkTimerCallback(object):
    def __init__(self, renderer, renWin, fps, _dir):
    # I can try putting most visualize commands here?
    # Move observer definitions here?
        self.timer_count = 1
        self.pause = False
        self.camera_flag = True
        
        self.renderer = renderer
        self.camera = vtkCamera()
        self.camera_distance = 14
        self.renderer.SetActiveCamera(self.camera)
        self.view = 1
        
        self.text_actor = draw_text('Init')
        self.renderer.AddActor(self.text_actor)
        
        if record_video_bool:
            self.fps = fps
            self.video_count = 1
            self._filter, self.writer = get_video(renWin, self.fps, 'M113_' + str(self.video_count), _dir)

        self.total_frame_counter = 1


    def keypress(self, obj, event):
        self.pause, self.camera_flag, self.camera_distance ,self.view, self.timer_count = keyboard_events(obj, self.pause, self.camera_flag, self.camera_distance, self.view, self.timer_count)


    def execute(self, obj, event):
        if self.timer_count < self.num_frames - 1:
            if self.pause == True:
                self.text_actor.SetInput('Pause')
                obj.GetRenderWindow().Render()

            else:
                if self.camera_flag:
                    if 'Slope' in self.dir:
                        # slope = np.rad2deg(max(0, 0.0044 * (self.timer_count*self.dt - 5)))
                        slope = 31
                        text = 'time = %.1f' % (self.timer_count * self.dt) + '[sec]'
                        self.text_actor.SetInput(text + '\n' + 'Slope Angle: ' + '{:.2f}'.format(slope) + '[deg]')
                    else:
                        slope = 0
                        text = 'time = %.1f' % (self.timer_count * self.dt) + '[sec]'
                        self.text_actor.SetInput(text)

                    if 'Step' in self.dir:
                        self.view = 5
                    elif 'Turning' in self.dir:
                        self.view = 4

                    place_camera(self.timer_count, self.data, self.camera, self.camera_distance, self.view, slope)

                place_all_bodies(self.data, self.timer_count)

                obj.GetRenderWindow().Render()
                
                # if self.timer_count > 5700:
                #     self.timer_count += 1
                #     self.total_frame_counter += 1
                # else:
                self.timer_count += 1
                self.total_frame_counter += 1

                if record_video_bool:
                    if self.total_frame_counter % 500 == 0:
                        self.writer.End()
                        self.video_count += 1
                        self._filter, self.writer = get_video(self.iren.GetRenderWindow(), self.fps, 'M113_' + str(self.video_count), self.dir)
                    self._filter.Modified()
                    self.writer.Write()

        else:
            self.timer_count = 0
            if record_video_bool:
                self.writer.End()
                self.iren.DestroyTimer()
                self.iren.GetRenderWindow().Finalize()
                self.iren.TerminateApp()
                print('Simulation End')
                return


def visualize(*args, directory, total_time = 25):
    # create renderer, figure and axes:
    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # add stationary axes:
    axesActor = vtkAxesActor()
    widget = vtkOrientationMarkerWidget()
    widget.SetOrientationMarker(axesActor)
    widget.SetInteractor(iren)
    widget.SetEnabled(1)
    widget.InteractiveOff()
    
    renderer.GradientBackgroundOn()
    renderer.SetBackground(0,0,0.5)
    renderer.SetBackground2(0.2,0.2,0.6)

    user32 = windll.user32
    resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    renWin.SetSize(resolution)

    # add all actors to the renderer
    for i in range(len(args)):
        for obj in args[i]:
            renderer.AddActor(obj.actor)

    surface = Surface(directory, args[0][0].path_loc)
    for actor in surface.actors:
        if actor:
            renderer.AddActor(actor)
        
    iren.Initialize()

    # Sign up to receive TimerEvent
    num_frames = args[0][0].path_loc.shape[0]
    FPS = int(round(num_frames/total_time))
    FPMS = FPS/1000 # frames/millisecond
    
    callback = vtkTimerCallback(renderer, renWin, FPS, directory)
    callback.data = args
    callback.ren = renderer
    callback.num_frames = args[0][0].path_dir.shape[0]
    callback.iren = iren
    callback.dt = total_time/callback.num_frames

    callback.dir = directory
    
    iren.AddObserver('TimerEvent', callback.execute)
    iren.AddObserver('KeyPressEvent', callback.keypress)
    
    iren.CreateRepeatingTimer(round(1/FPMS)) # milliseconds between frames
    iren.Start()
