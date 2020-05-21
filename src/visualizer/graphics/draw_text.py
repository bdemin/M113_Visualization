from vtk import vtkTextActor


def draw_text(_input):
    text_actor = vtkTextActor()
    text_actor.SetInput(_input)
    text_prop = text_actor.GetTextProperty()
    text_prop.SetFontFamilyToArial()
    text_prop.SetFontSize(34)
    text_prop.SetColor(1,1,1)
    text_actor.SetDisplayPosition(80,900)
    return text_actor
    