import numpy as np

from vtk import vtkRenderer, vtkRenderWindow, \
    vtkRenderWindowInteractor, vtkAxesActor, \
    vtkOrientationMarkerWidget

from .camera import Camera
from .graphics.draw_text import Text
from .graphics.get_video import get_video
from .input_handler import keyboard_events
# from .graphics.transformations import scale_actor


class vtkTimerCallback(object):
    # Change
    def __init__(self, visualizer):
    # Move observer definitions here?
        self.timer_count = 1
        self.pause = True
        self.video_record_flag = visualizer.video_record_flag
        
        self.camera = Camera()

        self.renderer = visualizer.renderer
        self.renderer.SetActiveCamera(self.camera)
        
        self.text = Text(self, visualizer.dt)
        
        if self.video_record_flag:
            self.rate = rate
            self.video_count = 1
            self._filter, self.writer = get_video(visualizer.renWin, self.rate, 'M113_' + str(self.video_count))

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
                obj.GetRenderWindow().Render()
            else:
                self.run_timestep()
        else:
            self.reset()
        self.text.update()
            
    def run_timestep(self):
        self.vehicle.update(self.timer_count)
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
