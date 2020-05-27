from vtk import vtkRenderer, vtkRenderWindow, \
    vtkRenderWindowInteractor, vtkAxesActor, \
    vtkOrientationMarkerWidget

from .callback import vtkTimerCallback


class Visualizer(object):
    def __init__(self, logic = None, vehicle = None, surface = None):
        self.vehicle = vehicle
        self.surface = surface

        if logic:
            self.video_record_flag = logic['record_video_flag']
        else:
            self.video_record_flag = False

        # Create renderer, figure and axes
        self.renderer = vtkRenderer()
        self.renWin = vtkRenderWindow()
        self.renWin.AddRenderer(self.renderer)
        self.iren = vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renWin)

        self.renderer.GradientBackgroundOn()
        self.renderer.SetBackground(0,0,0.5)
        self.renderer.SetBackground2(0.2,0.2,0.6)

        win_scale = 1/1.25
        win_size = (int(win_scale*1920), int(win_scale*1080))
        self.renWin.SetSize(win_size)

        # Add stationary axes
        # axesActor = vtkAxesActor()
        # scale_actor(axesActor, 4)
        # widget = vtkOrientationMarkerWidget()
        # widget.SetOrientationMarker(axesActor)
        # widget.SetInteractor(self.iren)
        # widget.SetEnabled(1)
        # widget.InteractiveOff()

    def add_actors(self):
        # Add all actors to the renderer

        if self.vehicle:
            for body_type in self.vehicle.data.values():
                for body in body_type:
                    self.renderer.AddActor(body.actor)

        for actor in self.surface.actors:
            self.renderer.AddActor(actor)

    def init_callback(self, total_time, num_frames):
        self.iren.Initialize()
        
        # Sign up to receive TimerEvent
        FPS = num_frames/total_time
        FPMS = FPS/1000
        
        callback = vtkTimerCallback(self.renderer, self.renWin, FPS, self.video_record_flag)
        callback.vehicle = self.vehicle
        callback.ren = self.renderer
        callback.num_frames = num_frames
        callback.iren = self.iren
        callback.dt = total_time/num_frames
        
        self.iren.AddObserver('TimerEvent', callback.run_main_loop)
        self.iren.AddObserver('KeyPressEvent', callback.keypress)
        
        self.iren.CreateRepeatingTimer(int(1/FPMS)) #ms
        self.iren.Start()
