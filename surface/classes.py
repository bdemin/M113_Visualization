import numpy as np

from vtk import vtkPoints, vtkCellArray, vtkTriangle, \
    vtkPolyData, vtkLookupTable, vtkCleanPolyData, \
    vtkUnsignedCharArray, vtkLoopSubdivisionFilter, \
    vtkPolyDataMapper, vtkActor, \
    vtkNamedColors

from surface.functions import visualize_elevation, visualize_soil, create_soil_type_arr, get_spline_actor


class Surface(object):
    def __init__(self, path = None, surface_data = None, logic = None, chassis_cg_path = None):

        # Load logic controls
        # color_map_flag = logic['color_map_flag'] # Create elevation-based colormap for the ground
        # soil_map_flag = logic['soil_map_flag'] # Create soil-based colormap for the ground
        # path_spline_flag = logic['path_spline_flag'] # Render a spline marking the vehicle's drive path

        surface_data = self.get_xyz_data(path, surface_data)
        self.surface_polydata = self.get_surface_polydata(surface_data)

        self.actors = []

        if logic:
            surface_polydata = self.apply_surface_filters(surface_polydata, logic)

            if logic['path_spline_flag']:
                self.actors.append(self.get_line_actor(surface_polydata, chassis_cg_path))

        self.actors.append(self.get_surface_actor(self.surface_polydata))
        
    def get_xyz_data(self, path, surface_data):
        # Return np arrays representing surface x,y,z data

        # Surface x,y,z data supplied from a folder
        if path:
            x_data = np.loadtxt(path + 'x.txt', delimiter = ',')
            y_data = np.loadtxt(path + 'y.txt', delimiter = ',')
            z_data = np.loadtxt(path + 'z.txt', delimiter = ',')
            # z_data -= 0.1 #fix ground clipping
            return x_data, y_data, z_data

        # Surface data supplied directly
        elif surface_data:
            return surface_data

        # Otherwise create surface data using external function
        from surface.functions import create_ground_from_spheres
        return create_ground_from_spheres()


    def get_surface_polydata(self, data):
        # Triangulate the data and return vtkPolyData object.
        
        x_data, y_data, z_data = data
        self.m = z_data.shape[0]
        self.n = z_data.shape[1]
        
        # Define points, triangles and colors
        points = vtkPoints()
        triangles = vtkCellArray()
        
        # Build the meshgrid (need to try Delauney)

        # profile = vtk.vtkPolyData()
        # profile.SetPoints(points)

        # Delaunay3D is used to triangulate the points. The Tolerance is the
        # distance that nearly coincident points are merged
        # together. (Delaunay does better if points are well spaced.) The
        # alpha value is the radius of circumcircles, circumspheres. Any mesh
        # entity whose circumcircle is smaller than this value is output.
        # from vtk import vtkDelaunay3D
        # delny = vtkDelaunay3D()
        # delny.SetInputData(profile)
        # delny.SetTolerance(0.01)
        # delny.SetAlpha(0.2)
        # delny.BoundingTriangulationOff()

        # Shrink the result to help see it better.
        # shrink = vtk.vtkShrinkFilter()
        # shrink.SetInputConnection(delny.GetOutputPort())
        # shrink.SetShrinkFactor(0.9)

        # map = vtk.vtkDataSetMapper()
        # map.SetInputConnection(shrink.GetOutputPort())

        # triangulation = vtk.vtkActor()
        # triangulation.SetMapper(map)
        # triangulation.GetProperty().SetColor(1, 0, 0)

        # ren.AddActor(triangulation)




        count = 0
        for i in range(self.m-1):
            for j in range(self.n-1):
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
        return PolyData


    def apply_surface_filters(self, PolyData, logic):
        if logic['color_map_flag']:
            visualize_elevation(PolyData)
            
        elif logic['soil_map_flag']:
            soil_type_array = create_soil_type_arr((self.m, self.n))
            visualize_soil(PolyData, soil_type_array)

        # Clean the polydata so that the edges are shared
        cleanPolyData = vtkCleanPolyData()
        cleanPolyData.SetInputData(PolyData)
        
        # Use a filter to smooth the data (will add triangles and smooth)
        smooth_loop = vtkLoopSubdivisionFilter()
        smooth_loop.SetNumberOfSubdivisions(3)
        smooth_loop.SetInputConnection(cleanPolyData.GetOutputPort())
        return smooth_loop
        
    def get_line_actor(self, smooth_loop, chassis_cg):
        return get_spline_actor(smooth_loop, chassis_cg)


    def get_surface_actor(self, smooth_loop):
        # Create a mapper and actor for smoothed dataset
        mapper = vtkPolyDataMapper()
        # mapper.SetInputConnection(smooth_loop.GetOutputPort())
        mapper.SetInputData(smooth_loop)
        
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
