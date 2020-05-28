import numpy as np

from vtk import vtkRenderer, vtkRenderWindow, \
    vtkRenderWindowInteractor, vtkAxesActor, \
    vtkOrientationMarkerWidget

from .graphics.draw_text import Text
from .graphics.get_video import get_video
from .input_handler import keyboard_events
# from .graphics.transformations import scale_actor

from .camera import Camera

class vtkTimerCallback(object):
    # Change
    # I can try putting most visualize commands here?
    def __init__(self, renderer, renWin, rate, video_record_flag, dt):
    # Move observer definitions here?

        self.timer_count = 1
        self.pause = True
        
        self.camera = Camera()

        self.renderer = renderer
        self.renderer.SetActiveCamera(self.camera)
        
        self.text = Text(dt)
        self.renderer.AddActor(self.text.actor)
        
        self.video_record_flag = video_record_flag
        if self.video_record_flag:
            self.rate = rate
            self.video_count = 1
            self._filter, self.writer = get_video(renWin, self.rate, 'M113_' + str(self.video_count))

    def run_main_loop(self, obj, event):
        # self.run_timestep()

        if self.camera.is_on:
            self.camera.place_camera(self.timer_count, self.vehicle.get_pos_and_dir)

        # self.vehicle.update(self.timer_count)
        if self.timer_count < self.num_frames - 1:
            obj.GetRenderWindow().Render()
            if self.video_record_flag:
                self.handle_video()

            if self.pause == True:
                self.text.pause(self.camera.current_view)
                obj.GetRenderWindow().Render()
            else:
                self.run_timestep()
        else:
            self.reset()
            
    def run_timestep(self):
        self.vehicle.update(self.timer_count)
        self.text.update(self.timer_count, self.camera.current_view)
        self.timer_count += 1

    def keypress(self, obj, event):
        self.pause, self.timer_count = \
            keyboard_events(obj, self.pause, self.camera, self.timer_count)


    def handle_video(self):
        if self.timer_count % 500 == 0:
            self.writer.End()
            self.video_count += 1
            self._filter, self.writer = get_video(self.iren.GetRenderWindow(), self.rate, 'M113_' + str(self.video_count))
        self._filter.Modified()
        self.writer.Write()

    def reset(self):
        self.timer_count = 0
        if self.video_record_flag:
                self.writer.End()
                self.iren.DestroyTimer()
                self.iren.GetRenderWindow().Finalize()
                self.iren.TerminateApp()
                print('Simulation End')
