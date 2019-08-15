import numpy as np

from vtk import vtkPoints, vtkCellArray, vtkTriangle, \
    vtkPolyData, vtkLookupTable, vtkCleanPolyData, \
    vtkUnsignedCharArray, vtkLoopSubdivisionFilter, \
    vtkPolyDataMapper, vtkActor, \
    vtkNamedColors

from graphics.ground import visualize_elevation, visualize_soil, create_soil_type_arr


color_map = False # Create elevation-based colormap for the ground
soil_map_bool = True # Create soil-based colormap for the ground

def get_3dsurface_actor(path_directory):
    path_directory = path_directory
    x_data = np.loadtxt(path_directory + 'x.txt', delimiter = ',')
    y_data = np.loadtxt(path_directory + 'y.txt', delimiter = ',')
    z_data = np.loadtxt(path_directory + 'z.txt', delimiter = ',')
    # z_data -= 0.1 #fix ground clipping
    
    m = z_data.shape[0]
    n = z_data.shape[1]
    
    # Define points, triangles and colors
    points = vtkPoints()
    triangles = vtkCellArray()
    
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
    
            triangle = vtkTriangle()
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
            
            triangle = vtkTriangle()
            triangle.GetPointIds().SetId(0, count + 3)
            triangle.GetPointIds().SetId(1, count + 4)
            triangle.GetPointIds().SetId(2, count + 5)
    
            count += 6
            triangles.InsertNextCell(triangle)
    
    # Create a polydata object
    PolyData = vtkPolyData()
    
    # Add the geometry and topology to the polydata
    PolyData.SetPoints(points)
    PolyData.SetPolys(triangles)
    
    if color_map:
        visualize_elevation(PolyData)
        
    elif soil_map_bool:
        soil_type_array = create_soil_type_arr((m, n))
        visualize_soil(PolyData, soil_type_array)

    # Clean the polydata so that the edges are shared
    cleanPolyData = vtkCleanPolyData()
    cleanPolyData.SetInputData(PolyData)
    
    # Use a filter to smooth the data (will add triangles and smooth)
    smooth_loop = vtkLoopSubdivisionFilter()
    smooth_loop.SetNumberOfSubdivisions(3)
    smooth_loop.SetInputConnection(cleanPolyData.GetOutputPort())
    
    # Create a mapper and actor for smoothed dataset
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(smooth_loop.GetOutputPort())
    
    actor_loop = vtkActor()
    actor_loop.SetMapper(mapper)
    
    actor_loop.GetProperty().SetAmbient(0.5)
    actor_loop.GetProperty().SetAmbientColor(0.1,0.1,0.1)

    # # actor_loop.GetProperty().SetInterpolationToPhong()
    actor_loop.GetProperty().SetDiffuse(0.5)
    actor_loop.GetProperty().SetDiffuseColor(0.1, 0.1, 0.1)
    # actor_loop.GetProperty().SetSpecular(10)
    actor_loop.GetProperty().SetSpecularPower(100)
    # actor_loop.GetProperty().SetSpecularColor(0.1,0.1,0.1)

    return actor_loop
    