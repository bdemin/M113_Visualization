import numpy as np

from vtk import vtkPoints, vtkCellArray, vtkTriangle, \
    vtkPolyData, vtkLookupTable, vtkCleanPolyData, \
    vtkUnsignedCharArray, vtkLoopSubdivisionFilter, \
    vtkPolyDataMapper, vtkActor, \
    vtkNamedColors

from graphics.ground import visualize_elevation, visualize_soil, create_soil_type_arr, get_spline_actor
from graphics.create_ground_from_spheres import create_ground_from_spheres

# Logic controls
color_map_bool = False # Create elevation-based colormap for the ground
soil_map_bool = True # Create soil-based colormap for the ground
path_spline_bool = True # Render a spline marking the vehicle's drive path

def get_3dsurface_actor(path_directory, ground_surf = None, chassis_cg = None):
    try:
        x_data = np.loadtxt(path_directory + 'x.txt', delimiter = ',')
        y_data = np.loadtxt(path_directory + 'y.txt', delimiter = ',')
        z_data = np.loadtxt(path_directory + 'z.txt', delimiter = ',')
        # z_data -= 0.1 #fix ground clipping
    except:
        if ground_surf != None:
            x_data, y_data, z_data = ground_surf
        else:
            x_data, y_data, z_data = create_ground_from_spheres()

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
    
    if color_map_bool:
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
    
    if path_spline_bool:
        line_actor = get_spline_actor(smooth_loop, chassis_cg, PolyData.GetBounds(), [0,0.7,0])
        # line_actor = None
        if 'Turning' in path_directory:
            chs_x = chassis_cg[:,0]
            chs_y = chassis_cg[:,1]
            center = [np.average(chs_x), np.average(chs_y)]
            thetas = np.linspace(0, 2 * np.pi, num = 50)
            # radius = np.average((np.abs(min(chs_x) - max(chs_x)), np.abs(min(chs_y)-max(chs_y))))/2
            radius = 6.88 # 5.9607

            circle = []
            for theta in thetas:
                x = center[0] + radius*np.cos(theta)
                y = center[1] + radius*np.sin(theta)
                circle.append([x, y, np.average(chassis_cg[:,2])])
            
            circle_actor = get_spline_actor(smooth_loop, np.array(circle), PolyData.GetBounds(), [0,0,0.7])
            # circle_actor = None
        else:
            circle_actor = None

    else:
        line_actor = None
        circle_actor = None

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
    return_data = [actor_loop, line_actor, smooth_loop, circle_actor]
    actors = []
    for data in return_data:
        if isinstance(data, vtkActor):
            actors.append(data)
    return actors
    