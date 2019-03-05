import vtk
import numpy as np

def get_3dsurface_actor(path_directory):
    path_directory = path_directory
    x_data = np.loadtxt(path_directory + 'x.txt', delimiter = ',')
    y_data = np.loadtxt(path_directory + 'y.txt', delimiter = ',')
    z_data = np.loadtxt(path_directory + 'z.txt', delimiter = ',')
    z_data -= 0.1 #fix ground clipping
    
    m = z_data.shape[0]
    n = z_data.shape[1]
    
    # Define points, triangles and colors
    points = vtk.vtkPoints()
    triangles = vtk.vtkCellArray()
    
    # Build the meshgrid:
    #need to try Delauney
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
    trianglePolyData = vtk.vtkPolyData()
    
    # Add the geometry and topology to the polydata
    trianglePolyData.SetPoints(points)
    #trianglePolyData.GetPointData().SetScalars(colors)
    trianglePolyData.SetPolys(triangles)
    
    # Clean the polydata so that the edges are shared !
    cleanPolyData = vtk.vtkCleanPolyData()
    cleanPolyData.SetInputData(trianglePolyData)
    
    # Use a filter to smooth the data (will add triangles and smooth)
    smooth_loop = vtk.vtkLoopSubdivisionFilter()
    smooth_loop.SetNumberOfSubdivisions(3)
    smooth_loop.SetInputConnection(cleanPolyData.GetOutputPort())
    
  
    res = 10
    tableSize = res*res + 1
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(tableSize)
    lut.Build()
    
    #Fill in a few known colors, the rest will be generated if needed
    lut.SetTableValue(0     , 0     , 0     , 0, 1)  #Black
    lut.SetTableValue(1, 0.8900, 0.8100, 0.3400, 1) # Banana
    lut.SetTableValue(2, 1.0000, 0.3882, 0.2784, 1) # Tomato
    lut.SetTableValue(3, 0.9608, 0.8706, 0.7020, 1) # Wheat
    lut.SetTableValue(4, 0.9020, 0.9020, 0.9804, 1) # Lavender
    lut.SetTableValue(5, 1.0000, 0.4900, 0.2500, 1) # Flesh
    lut.SetTableValue(6, 0.5300, 0.1500, 0.3400, 1) # Raspberry
    lut.SetTableValue(7, 0.9804, 0.5020, 0.4471, 1) # Salmon
    lut.SetTableValue(8, 0.7400, 0.9900, 0.7900, 1) # Mint
    lut.SetTableValue(9, 0.2000, 0.6300, 0.7900, 1) # Peacock
    
    
    
    
    # Create a mapper and actor for smoothed dataset
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(smooth_loop.GetOutputPort())
    
    mapper.SetScalarRange(0, tableSize - 1)
    mapper.SetLookupTable(lut)
    
    actor_loop = vtk.vtkActor()
    actor_loop.SetMapper(mapper)
    
#    actor_loop.GetProperty().SetColor(0.929, 0.788, 0.686)
#    actor_loop.GetProperty().SetAmbient(0.1)
#    actor_loop.GetProperty().SetAmbientColor(0.3,0.3,0.3)
    
#    actor_loop.GetProperty().SetDiffuse(0.1)
#    actor_loop.GetProperty().SetDiffuseColor(0.396, 0.263, 0.129)
#    actor_loop.GetProperty().SetInterpolationToPhong()
#    actor_loop.GetProperty().SetSpecular(0.6)
#    actor_loop.GetProperty().SetSpecularPower(10)
#    actor_loop.GetProperty().EdgeVisibilityOn()
    
#    actor_loop.GetProperty().SetLineWidth(0.2)

    return actor_loop