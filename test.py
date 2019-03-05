import vtk
import numpy as np


path_directory = 'INPUT/Simulation_5/'

x_data = np.loadtxt(path_directory + 'x.txt', delimiter = ',')
y_data = np.loadtxt(path_directory + 'y.txt', delimiter = ',')
z_data = np.loadtxt(path_directory + 'z.txt', delimiter = ',')
z_data = z_data * 100
#    z_data -= 0.05 #fix ground clipping

m = z_data.shape[0]
n = z_data.shape[1]

# Define points, triangles and colors
points = vtk.vtkPoints()
triangles = vtk.vtkCellArray()

# Build the meshgrid:
count = 0
for i in range(m-1):
    for j in range(n-1):
        z1 = z_data[i][j]
        z2 = z_data[i][j+1]
        z3 = z_data[i+1][j]

        # Triangle 1
        points.InsertNextPoint(x_data[i], y_data[j], z1)
        points.InsertNextPoint(x_data[i], y_data[j+1], z2)
        points.InsertNextPoint(x_data[i+1], y_data[j], z3)

        triangle = vtk.vtkTriangle()
        triangle.GetPointIds().SetId(0, count)
        triangle.GetPointIds().SetId(1, count + 1)
        triangle.GetPointIds().SetId(2, count + 2)

        triangles.InsertNextCell(triangle)
        
        z1 = z_data[i][j+1]
        z2 = z_data[i+1][j+1]
        z3 = z_data[i+1][j]

        # Triangle 2  
        points.InsertNextPoint(x_data[i], y_data[j+1], z1)
        points.InsertNextPoint(x_data[i+1], y_data[j+1], z2)
        points.InsertNextPoint(x_data[i+1], y_data[j], z3)
        
        triangle = vtk.vtkTriangle()
        triangle.GetPointIds().SetId(0, count + 3)
        triangle.GetPointIds().SetId(1, count + 4)
        triangle.GetPointIds().SetId(2, count + 5)

        count += 6

        triangles.InsertNextCell(triangle)

# Create a polydata object
PolyData = vtk.vtkPolyData()

# Add the geometry and topology to the polydata
PolyData.SetPoints(points)
#trianglePolyData.GetPointData().SetScalars(colors)
PolyData.SetPolys(triangles)





# Colour transfer function.
ctf = vtk.vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
colors = vtk.vtkNamedColors()
p1 = [0.0] + list(colors.GetColor3d("MidnightBlue"))
p2 = [1.0] + list(colors.GetColor3d("DarkOrange"))
ctf.AddRGBPoint(*p1)
ctf.AddRGBPoint(*p2)
cc = list() #color range
for i in range(256):
    cc.append(ctf.GetColor(float(i) / 255.0))
        
bounds = PolyData.GetBounds()
minz = bounds[4]
maxz = bounds[5]
lut = vtk.vtkLookupTable()
lut.SetNumberOfColors(256)
for i, item in enumerate(cc):
    lut.SetTableValue(i, item[0], item[1], item[2], 1.0)
#lut.SetTableRange(minz, maxz)
lut.Build()

    
#colors = vtk.vtkUnsignedCharArray()
#colors.SetNumberOfComponents(3)
#colors.SetName('Colors')

#for i in range(PolyData.GetNumberOfPoints()):
#    point = PolyData.GetPoint(i)
#    dcolor = 3*[0.0]
#    lut.GetColor(point[2], dcolor) #assign color to z value
#    color = [i*255.0 for i in dcolor]
#    colors.InsertNextTuple3(*color)
    
#PolyData.GetPointData().SetScalars(colors)

cleanPolyData = vtk.vtkCleanPolyData()
cleanPolyData.SetInputData(PolyData)

smoothPolyData = vtk.vtkLoopSubdivisionFilter()
smoothPolyData.SetNumberOfSubdivisions(3)
smoothPolyData.SetInputConnection(cleanPolyData.GetOutputPort())

mapper = vtk.vtkPolyDataMapper()
#mapper.SetInputData(PolyData)
mapper.SetInputConnection(smoothPolyData.GetOutputPort())


mapper.SetLookupTable(lut)
mapper.SetUseLookupTableScalarRange(1)
        
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create a mapper and actor for smoothed dataset
#mapper = vtk.vtkPolyDataMapper()
#mapper.SetInputConnection(trianglePolyData.GetOutputPort())

#actor.GetProperty().SetColor(0.929, 0.788, 0.686)
#actor.GetProperty().SetAmbient(0.1)
#actor.GetProperty().SetAmbientColor(0.3,0.3,0.3)
#
#actor_loop.GetProperty().SetDiffuse(0.1)
#actor_loop.GetProperty().SetDiffuseColor(0.396, 0.263, 0.129)
#actor_loop.GetProperty().SetInterpolationToPhong()
#actor_loop.GetProperty().SetSpecular(0.6)
#actor_loop.GetProperty().SetSpecularPower(10)
#actor.GetProperty().EdgeVisibilityOn()
#
#actor.GetProperty().SetLineWidth(0.2)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renderer.GradientBackgroundOn()
renderer.SetBackground(0,0,0.5)
renderer.SetBackground2(0.2,0.2,0.6)
renWin.SetSize(1800, 1200)

renderer.AddActor(actor)

iren.Initialize()
iren.Start()    