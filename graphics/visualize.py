import numpy as np

from vtk import vtkCamera, vtkRenderer, vtkRenderWindow, \
    vtkRenderWindowInteractor, vtkAxesActor, \
    vtkOrientationMarkerWidget

from graphics.place_camera import place_camera
from graphics.place_object import place_all_bodies
from graphics.transformations import scale_actor
from graphics.draw_text import draw_text

from helpers.event_handling import keyboard_events

from bodies.classes import Surface

from graphics.get_video import get_video, get_snapshots, snap


record_video_bool = True

class vtkTimerCallback(object):
    def __init__(self, renderer, renWin, rate):
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
            self.rate = rate
            self.video_count = 1
            self._filter, self.writer = get_video(renWin, self.rate, 'M113_' + str(self.video_count))


    def keypress(self, obj, event):
        self.pause, self.camera_flag, self.camera_distance ,self.view, self.timer_count = keyboard_events(obj, self.pause, self.camera_flag, self.camera_distance, self.view, self.timer_count)


    def execute(self, obj, event):
        if self.camera_flag:
            place_camera(self.timer_count, self.data, self.camera, self.camera_distance, self.view)

        place_all_bodies(self.data, self.timer_count)

        if self.timer_count < self.num_frames - 1:
            obj.GetRenderWindow().Render()
            if record_video_bool:
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
            if record_video_bool:
                self.writer.End()
                self.timer_count = 0
                self.iren.DestroyTimer()
                self.iren.GetRenderWindow().Finalize()
                self.iren.TerminateApp()
                print('Simulation End')

            text = 'time = %.1fs' % (self.timer_count * self.dt)
            self.text_actor.SetInput(text)


def visualize(*args, directory, total_time = 25):
    # create renderer, figure and axes:
    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # add stationary axes:    
    axesActor = vtkAxesActor()
    scale_actor(axesActor, 4)
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

    surface = Surface(directory, args[0][0].path_loc)
    for actor in surface.actors:
        if actor:
            renderer.AddActor(actor)
        
    iren.Initialize()

    # Sign up to receive TimerEvent
    num_frames = args[0][0].path_loc.shape[0]
    FPS = num_frames/total_time
    FPMS = FPS/1000
    
    callback = vtkTimerCallback(renderer, renWin, FPS)
    callback.data = args
    callback.ren = renderer
    callback.num_frames = args[0][0].path_dir.shape[0]
    callback.iren = iren
    callback.dt = total_time/callback.num_frames
    
    iren.AddObserver('TimerEvent', callback.execute)
    iren.AddObserver('KeyPressEvent', callback.keypress)
    
    iren.CreateRepeatingTimer(int(1/FPMS)) #ms
    iren.Start()
