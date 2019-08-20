import numpy as np
import vtk

from graphics.create_ground_from_sphere import create_ground_from_spheres
from graphics.get_3dsurface_actor import get_3dsurface_actor


ground_data = create_ground_from_spheres()
surface_actor, smooth_loop = get_3dsurface_actor(None, ground_data)

# Update the pipeline so that vtkCellLocator finds cells !
smooth_loop.Update()

# Define a cellLocator to be able to compute intersections between lines
# and the surface
locator = vtk.vtkCellLocator()
locator.SetDataSet(smooth_loop.GetOutput())
locator.BuildLocator()

maxloop = 1000

dist = 19/maxloop
tolerance = 0.001

# Make a list of points. Each point is the intersection of a vertical line
# defined by p1 and p2 and the surface.
points = vtk.vtkPoints()
for i in range(maxloop):

    p1 = [-19 + i*dist, -19 + i*dist, -1]
    p2 = [-19 + i*dist, -19 + i*dist, 0]

    t = vtk.mutable(0)
    pos = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    subId = vtk.mutable(0)
    locator.IntersectWithLine(p1, p2, tolerance, t, pos, pcoords, subId)

    # Add a slight offset in z
    pos[2] += 0.05
    
    # Add the x, y, z position of the intersection
    points.InsertNextPoint(pos)

# Create a spline and add the points
spline = vtk.vtkParametricSpline()
spline.SetPoints(points)
functionSource = vtk.vtkParametricFunctionSource()
functionSource.SetUResolution(maxloop)
functionSource.SetParametricFunction(spline)

# Map the spline
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(functionSource.GetOutputPort())

# Define the line actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor([0.3, 0.3, 1.0])
actor.GetProperty().SetLineWidth(6)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renderer.GradientBackgroundOn()
renderer.SetBackground(0,0,0.5)
renderer.SetBackground2(0.2,0.2,0.6)
scale = 0.8
screen_size = (1920*scale, 1080*scale)
renWin.SetSize(int(scale*1920), int(scale*1080))

renderer.AddActor(surface_actor)    
renderer.AddActor(actor)        
iren.Initialize()
iren.Start()