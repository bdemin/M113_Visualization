from PIL import Image
import vtk

from src.surface.surface import Surface

path = '../Eitan/Results/3D_Terrain_Movie2/'

logic = dict()
logic['color_map_flag'] = None
logic['soil_map_flag'] = None
logic['path_spline_flag'] = None

surface = Surface(path, None, logic, None)
num_points = surface.surface_polydata.GetNumberOfPoints()

im_file = 'resources/textures/ground4.jpg'
im = Image.open(im_file, 'r')
# im = im.resize((699, 299))
# pix_val = list(im.getdata())

soil_color_map = vtk.vtkUnsignedCharArray()
soil_color_map.SetNumberOfComponents(3)
soil_color_map.SetName("Colors")

img_i = 0
img_j = 0
# m = 292 - 1 = 291
# n = 361 - 1 = 360
# number of triangles = 104760
# number of points = 628560
for surf_i in range(surface.m - 1):
    for surf_j in range(surface.n - 1):
        for _ in range(6):
            soil_color_map.InsertNextTypedTuple(im.getpixel((img_i, img_j)))
            
        if img_j >= im.height - 1:
            img_j = 0
        else:
            img_j += 1
    img_j = 0
    if img_i >= im.width - 1:
        img_i = 0
    else:
        img_i += 1

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
