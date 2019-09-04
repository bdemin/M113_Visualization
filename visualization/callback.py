from vtk import vtkCamera

from visualization.place_camera import place_camera
from visualization.place_object import place_all_bodies
from visualization.transformations import scale_actor
from visualization.draw_text import draw_text
from visualization.get_video import get_video, get_snapshots, snap

from visualization.event_handling import keyboard_events


class vtkTimerCallback(object):
    def __init__(self, renderer, renWin, rate, video_record_flag):
    # I can try putting most visualize commands here?
    # Move observer definitions here?
        self.timer_count = 1
        self.pause = True
        self.camera_flag = True
        
        self.renderer = renderer
        self.camera = vtkCamera()
        self.camera_distance = 14
        self.renderer.SetActiveCamera(self.camera)
        self.view = 1
        
        self.text_actor = draw_text('Init')
        self.renderer.AddActor(self.text_actor)
        
        if video_record_flag:
            self.rate = rate
            self.video_count = 1
            self._filter, self.writer = get_video(renWin, self.rate, 'M113_' + str(self.video_count))


    def keypress(self, obj, event):
        self.pause, self.camera_flag, self.camera_distance ,self.view, self.timer_count = keyboard_events(obj, self.pause, self.camera_flag, self.camera_distance, self.view, self.timer_count)


    def execute(self, obj, event):
        if self.camera_flag:
            place_camera(self.timer_count, self.data, self.camera, self.camera_distance, self.view)

        place_all_bodies(self.data, self.timer_count)

        # if 0 <= self.timer_count and self.timer_count < int(self.num_frames - 1):
        if self.timer_count < self.num_frames - 1:
            obj.GetRenderWindow().Render()
            if video_record_flag:
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
            if video_record_flag:
                self.writer.End()
            self.timer_count = 0
            self.iren.DestroyTimer()
            self.iren.GetRenderWindow().Finalize()
            self.iren.TerminateApp()
            print('Simulation End')