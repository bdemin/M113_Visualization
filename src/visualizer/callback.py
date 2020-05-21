import numpy as np

from vtk import vtkCamera, vtkRenderer, vtkRenderWindow, \
    vtkRenderWindowInteractor, vtkAxesActor, \
    vtkOrientationMarkerWidget

from .graphics.place_camera import place_camera
from .graphics.draw_text import draw_text
from .graphics.get_video import get_video
from .event_handling import keyboard_events
# from .graphics.transformations import scale_actor


class vtkTimerCallback(object):
    def __init__(self, renderer, renWin, rate, video_record_flag):
    # I can try putting most visualize commands here?
    # Move observer definitions here?
        self.timer_count = 1
        self.cam_view = 'isometric'
        self.pause = True
        self.is_cam_on = True
        
        self.renderer = renderer
        self.camera = vtkCamera()
        self.camera_distance = 14
        self.renderer.SetActiveCamera(self.camera)
        self.view = 1
        
        self.text_actor = draw_text('Init')
        self.renderer.AddActor(self.text_actor)
        
        self.video_record_flag = video_record_flag
        if self.video_record_flag:
            self.rate = rate
            self.video_count = 1
            self._filter, self.writer = get_video(renWin, self.rate, 'M113_' + str(self.video_count))

    def run_main_loop(self, obj, event):
        # self.run_timestep()

        if self.is_cam_on:
            place_camera(self.timer_count, self.vehicle.data, self.camera, self.cam_dist, self.cam_view)

        self.vehicle.update(self.timer_count)

        # if 0 <= self.timer_count and self.timer_count < int(self.num_frames - 1):
        if self.timer_count < self.num_frames - 1:
            obj.GetRenderWindow().Render()
            if self.video_record_flag:
                self.handle_video()

            if self.pause == True:
                self.text_actor.SetInput('Pause')
                obj.GetRenderWindow().Render()
            else:
                self.run_timestep()
        else:
            self.reset()
            
    def run_timestep(self):
        self.vehicle.update(self.timer_count)
        text = 'time = %.1fs' % (self.timer_count * self.dt)
        self.text_actor.SetInput(text)
        self.timer_count += 1

    def keypress(self, obj, event):
        self.pause, self.is_cam_on, self.cam_dist ,self.cam_view, self.timer_count = keyboard_events(obj, self.pause, self.is_cam_on, self.cam_dist, self.cam_view, self.timer_count)


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
