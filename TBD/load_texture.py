from PIL import Image
import vtk

from surface.classes import Surface


surface = Surface(None, None, None, None)
num_points = surface.surface_polydata.GetNumberOfPoints()

im_file = 'ground1.jpg'
im = Image.open(im_file, 'r')
im = im.resize((699, 299))
pix_val = list(im.getdata())

soil_color_map = vtk.vtkUnsignedCharArray()
soil_color_map.SetNumberOfComponents(3)
soil_color_map.SetName("Colors")

for i in range(299*699):
    for _ in range(6):
        soil_color_map.InsertNextTypedTuple(pix_val[i])

surface.surface_polydata.GetPointData().SetScalars(soil_color_map)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renderer.GradientBackgroundOn()
renderer.SetBackground(0,0,0.5)
renderer.SetBackground2(0.2,0.2,0.6)

renderer.AddActor(surface.actors[0])

win_scale = 1/1.25
win_size = (int(win_scale*1920), int(win_scale*1080))
renWin.SetSize(win_size)

renWin.Render()
iren.Initialize()
iren.Start()
