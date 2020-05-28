from vtk import vtkTextActor


class Text(object):
    def __init__(self, dt):
        #

        self.dt = dt
        self.actor = vtkTextActor()
        text_prop = self.actor.GetTextProperty()
        text_prop.SetFontFamilyToArial()
        text_prop.SetFontSize(34)
        text_prop.SetColor(1,1,1)
        self.actor.SetDisplayPosition(80,600)

        self.actor.SetInput('Visualization ready')

