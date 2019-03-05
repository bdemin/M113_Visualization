import vtk
import numpy as np

#color_map = True
color_map = False

def get_surface_actor(width, resolution, y_offset, path_directory):
#    data = np.loadtxt(path_directory + 'Ground_Rock2Dlight.txt', delimiter = ',')
    data = np.loadtxt(path_directory, delimiter = ',')
    x_coords = data[:,0]
    y_coords = np.linspace(y_offset - width/2, y_offset + width/2, num=resolution)
    z_coords = data[:,1]
    z_coords -= 0.05 #fix ground clipping
    
    m = x_coords.shape[0]
    n = y_coords.shape[0]
    
    # Define points, triangles and colors
    points = vtk.vtkPoints()
    triangles = vtk.vtkCellArray()
    
    # Build the meshgrid manually
    count = 0
    for i in range(m-1):
        for j in range(n-1):
            z1 = z_coords[i]
            z2 = z_coords[i]
            z3 = z_coords[i+1]
    
            # Triangle 1
            points.InsertNextPoint(x_coords[i], y_coords[j], z1)
            points.InsertNextPoint(x_coords[i], y_coords[j+1], z2)
            points.InsertNextPoint(x_coords[i+1], y_coords[j], z3)
    
            triangle = vtk.vtkTriangle()
            triangle.GetPointIds().SetId(0, count)
            triangle.GetPointIds().SetId(1, count + 1)
            triangle.GetPointIds().SetId(2, count + 2)
    
            triangles.InsertNextCell(triangle)
            
            z1 = z_coords[i]
            z2 = z_coords[i+1]
            z3 = z_coords[i+1]
    
            # Triangle 2  
            points.InsertNextPoint(x_coords[i], y_coords[j+1], z1)
            points.InsertNextPoint(x_coords[i+1], y_coords[j+1], z2)
            points.InsertNextPoint(x_coords[i+1], y_coords[j], z3)
            
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
    #PolyData.GetPointData().SetScalars(colors)
    PolyData.SetPolys(triangles)
    
    if color_map:
        bounds = PolyData.GetBounds()
        minz = bounds[4]
        maxz = bounds[5]
        lut = vtk.vtkLookupTable()
        lut.SetTableRange(minz, maxz)
        lut.Build()
        
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName('Colors')
        
        for i in range(PolyData.GetNumberOfPoints()):
            point = PolyData.GetPoint(i)
            dcolor = 3*[0.0]
            lut.GetColor(point[2], dcolor) #assign color to z value
            color = [i*255.0 for i in dcolor]
            colors.InsertNextTuple3(*color)
            
        PolyData.GetPointData().SetScalars(colors)
        
    # Clean the polydata so that the edges are shared !
    cleanPolyData = vtk.vtkCleanPolyData()
    cleanPolyData.SetInputData(PolyData)
    
    # Use a filter to smooth the data (will add triangles and smooth)
    smoothPolyData = vtk.vtkLoopSubdivisionFilter()
    smoothPolyData.SetNumberOfSubdivisions(3)
    smoothPolyData.SetInputConnection(cleanPolyData.GetOutputPort())
    
    # Create a mapper and actor for smoothed dataset
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(smoothPolyData.GetOutputPort())
    actor_loop = vtk.vtkActor()
    actor_loop.SetMapper(mapper)
    
    actor_loop.GetProperty().SetColor(0.929, 0.788, 0.686)
    actor_loop.GetProperty().SetAmbient(0.1)
    actor_loop.GetProperty().SetAmbientColor(0.3,0.3,0.3)
#    actor_loop.GetProperty().SetDiffuse(0.1)
#    actor_loop.GetProperty().SetDiffuseColor(0.396, 0.263, 0.129)
#    actor_loop.GetProperty().SetInterpolationToPhong()
#    actor_loop.GetProperty().SetSpecular(0.6)
#    actor_loop.GetProperty().SetSpecularPower(10)
#    actor_loop.GetProperty().EdgeVisibilityOn()
    actor_loop.GetProperty().SetLineWidth(0.2)

    return actor_loop