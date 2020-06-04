from vtk import vtkTextActor


class Text(object):
    def __init__(self, callback, dt):
        self.text = 4*[None]
        self.actor = vtkTextActor()
        text_prop = self.actor.GetTextProperty()
        text_prop.SetFontFamilyToArial()
        text_prop.SetFontSize(28)
        text_prop.SetColor(1,1,1)
        self.actor.SetDisplayPosition(40,800)

        self.dt = dt
        self.callback = callback
        self.callback.renderer.AddActor(self.actor)

        self.update()
        
    def update(self):
        # Update text with new callback data

        self.text[0] = 'Paused' if self.callback.pause \
            else ''
        self.text[1] = 'Time = %.1f seconds' % (self.callback.timer_count * self.dt)
        self.text[2] = f'Current view: {self.callback.camera.current_view}'
        self.text[3] = 'Camera enabled' if self.callback.camera.is_on \
            else 'Camera disabled'
        self.actor.SetInput('\n'.join(self.text))
