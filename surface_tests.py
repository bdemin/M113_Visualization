import numpy as np
import vtk


def Create_Ground():
    size_x = 50; size_y = 50
    max_r = 6; min_r = 1

    GroundSurf = np.zeros((size_x, size_y))
    num_spheres = 3000
    for i in range(num_spheres):
        x0 = round(size_x * np.random.rand())
        y0 = round(size_y * np.random.rand())
        rand_rad = (max_r - min_r) * np.random.rand()
        for x1 in range(x0 - round(rand_rad), x0 + round(rand_rad)):
            for y1 in range(y0 - round(rand_rad), y0 + round(rand_rad)):
                if x1>0 and x1<size_x and y1>0 and y1<size_y:
                    z_add = rand_rad**2 - ((x1-x0)**2 + (y1-y0)**2)
                    if z_add > 0:
                        GroundSurf[x1,y1] = GroundSurf[x1,y1] + z_add

    z_max = np.max(GroundSurf)
    z_min = np.min(GroundSurf)
    scale_factor = 1.2
    for i in range(size_x):
        for j in range(size_y):
            GroundSurf[i,j] = ((GroundSurf[i,j] - z_min)/(z_max - z_min))*scale_factor - 1

    GroundSurf[:,0] = np.arange(-20, -20 + size_x*0.2, 0.2)
    GroundSurf[0,:] = np.arange(-20, -20 + size_y*0.2, 0.2)
    return GroundSurf


def get_3dsurface_actor(data):
    color_map = True
    # color_map = False
    x_data = data[:,0]
    y_data = data[0,:]
    z_data = data[1:-2, 1:-2]
    
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
    PolyData = vtk.vtkPolyData()
    
    # Add the geometry and topology to the polydata
    PolyData.SetPoints(points)
    PolyData.SetPolys(triangles)
    
    if color_map:
        #%% Create colormap
        bounds= 6*[0.0]
        PolyData.GetBounds(bounds)

        # Find min and max z
        minz = bounds[4]
        maxz = bounds[5]


        colorSeries = vtk.vtkColorSeries()
        # colorSeriesEnum = colorSeries.BREWER_QUALITATIVE_SET3
        # colorSeries.SetColorScheme(colorSeriesEnum)
        

        colorLookupTable = vtk.vtkLookupTable()
        colorLookupTable.SetTableRange(minz, maxz)
        colorLookupTable.Build()
        for i in range(10,20):
            print(colorLookupTable.GetTableValue(i))
        colorSeries.BuildLookupTable(colorLookupTable)
        

        for i in range(10,20):
            print(colorLookupTable.GetTableValue(i))

        # Generate the colors for each point based on the color map
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
            
        for i in range(0, PolyData.GetNumberOfPoints()):
            p = 3*[0.0]
            PolyData.GetPoint(i,p)

            dcolor = 3*[0.0]
            colorLookupTable.GetColor(p[2], dcolor)

            color=3*[0.0]
            for j in range(3):
                color[j] = int(255.0 * dcolor[j])

            colors.InsertNextTypedTuple(color)

        # PolyData.GetPointData().SetScalars(colors)


    # Clean the polydata so that the edges are shared !
    cleanPolyData = vtk.vtkCleanPolyData()
    cleanPolyData.SetInputData(PolyData)
    
    # Use a filter to smooth the data (will add triangles and smooth)
    smooth_loop = vtk.vtkLoopSubdivisionFilter()
    smooth_loop.SetNumberOfSubdivisions(3)
    smooth_loop.SetInputConnection(cleanPolyData.GetOutputPort())
    
    # Create a mapper and actor for smoothed dataset
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(smooth_loop.GetOutputPort())
    
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



ground_data = Create_Ground()
surface_actor = get_3dsurface_actor(ground_data)

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
iren.Initialize()
iren.Start()