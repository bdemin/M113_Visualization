import vtk
import numpy as np

def create_surface():
    path_directory = 'PATH2D/'
    #elevation_data = np.loadtxt(path_directory + 'Ground_Rock2D.txt', delimiter = ',')
    topography = np.loadtxt(path_directory + 'Ground_Rock2D_2.txt')
#    topography *= 10
    #elevation_data = elevation_data[:,1]
    #elevation_data *= 100
    #width = elevation_data.shape[0]
    #width = 30
    
    #topography = np.repeat(elevation_data, width).reshape((width, elevation_data.shape[0]))
    
    m = topography.shape[0]
    n = topography.shape[1]
    
    # Define points, triangles and colors
    points = vtk.vtkPoints()
    triangles = vtk.vtkCellArray()
    
    # Build the meshgrid manually
    count = 0
    for i in range(m-1):
        for j in range(n-1):
    
            z1 = topography[i][j]
            z2 = topography[i][j+1]
            z3 = topography[i+1][j]
    
            # Triangle 1
            points.InsertNextPoint(i, j, z1)
            points.InsertNextPoint(i, (j+1), z2)
            points.InsertNextPoint((i+1), j, z3)
    
            triangle = vtk.vtkTriangle()
            triangle.GetPointIds().SetId(0, count)
            triangle.GetPointIds().SetId(1, count + 1)
            triangle.GetPointIds().SetId(2, count + 2)
    
            triangles.InsertNextCell(triangle)
    
            z1 = topography[i][j+1]
            z2 = topography[i+1][j+1]
            z3 = topography[i+1][j]
    
            # Triangle 2
            points.InsertNextPoint(i, (j+1), z1)
            points.InsertNextPoint((i+1), (j+1), z2)
            points.InsertNextPoint((i+1), j, z3)
    
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
    
    # Create a mapper and actor for smoothed dataset
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(smooth_loop.GetOutputPort())
    actor_loop = vtk.vtkActor()
    actor_loop.SetMapper(mapper)
    actor_loop.GetProperty().SetInterpolationToFlat()
    
    # Update the pipeline so that vtkCellLocator finds cells !
    smooth_loop.Update()
    
    # Define a cellLocator to be able to compute intersections between lines
    # and the surface
    locator = vtk.vtkCellLocator()
    locator.SetDataSet(smooth_loop.GetOutput())
    locator.BuildLocator()
    
    transform = vtk.vtkTransform()
    transform.Scale((0.06, 1, 1))
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetTransform(transform)
    actor_loop.SetUserTransform(transform)

    # Visualize
#    renderer = vtk.vtkRenderer()
#    renderWindow = vtk.vtkRenderWindow()
#    renderWindow.AddRenderer(renderer)
#    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
#    renderWindowInteractor.SetRenderWindow(renderWindow)
    
    return actor_loop
    # Add actors and render
#    renderer.AddActor(actor_loop)
#    
#    renderer.SetBackground(1, 1, 1)  # Background color white
#    renderWindow.SetSize(800, 800)
#    renderWindow.Render()
#    renderWindowInteractor.Start()