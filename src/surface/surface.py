import numpy as np
from os.path import exists

from vtk import vtkPoints, vtkCellArray, vtkTriangle, \
    vtkPolyData, vtkLookupTable, vtkCleanPolyData, \
    vtkUnsignedCharArray, vtkLoopSubdivisionFilter, \
    vtkPolyDataMapper, vtkActor, \
    vtkNamedColors

# from .functions import visualize_elevation, visualize_soil, create_soil_type_arr, get_spline_actor, map_texture
from .functions import *


class Surface(object):
    def __init__(self, path = None, surface_xyz_data = None, logic = None, chassis_cg_path = None):
        # Class for creating and manipulating the surface/ground.

        self.path = path

        if surface_xyz_data: # Create surface from external data
            self.surface_polydata = self.get_surface_polydata(surface_xyz_data)

        else:
            if all(( # Create surface from simulation data
                exists(path + 'x.txt'),
                exists(path + 'y.txt'),
                exists(path + 'z.txt'))):
                    self.surface_polydata = self.get_surface_polydata(self.load_xyz_data_from_path(path))

            else: # Otherwise create surface data using external function
                from .functions import get_random_surface_xyz_data
                import warnings
                warnings.warn('No surface data found in ', self.path)
                self.surface_polydata = self.get_surface_polydata(get_random_surface_xyz_data())

        self.actors = []

        # Load surface logic controls
        color_map_flag = logic['color_map_flag'] # Create elevation-based colormap for the ground
        soil_map_flag = logic['soil_map_flag'] # Create soil-based colormap for the ground
        path_spline_flag = logic['path_spline_flag'] # Render a spline marking the vehicle's drive path

        if logic:
            surface_polydata = self.apply_surface_filters(self.surface_polydata, logic, chassis_cg_path)
            
        self.actors.append(self.get_surface_actor(self.surface_polydata))
        
    def get_surface_polydata(self, xyz_data):
        # Triangulate the data and return vtkPolyData object.
        
        x_data, y_data, z_data = xyz_data
        x_data, y_data = y_data, x_data
        z_data = np.transpose(z_data)
        self.m = z_data.shape[0]
        self.n = z_data.shape[1]
        
        # Define points, triangles and colors
        points = vtkPoints()
        triangles = vtkCellArray()
        
        # Build the meshgrid (need to try Delauney)
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

    @staticmethod
    def load_xyz_data_from_path(path):
        # Return np arrays representing surface x,y,z data
        
        x_data = np.loadtxt(path + 'x.txt', delimiter = ',')
        y_data = np.loadtxt(path + 'y.txt', delimiter = ',')
        z_data = np.loadtxt(path + 'z.txt', delimiter = ',')
        # z_data -= 0.1 # Fix ground clipping

        return x_data, y_data, z_data

    def apply_surface_filters(self, PolyData, logic, chassis_ch_path):
        if logic['color_map_flag']:
            visualize_elevation(PolyData)
            
        elif logic['soil_map_flag']:
            soil_type_array = create_soil_type_arr((self.m, self.n))
            visualize_soil(PolyData, soil_type_array)

        elif logic['path_spline_flag']:
                self.actors.append(self.get_line_actor(surface_polydata, chassis_cg_path))

        # Clean the polydata so that the edges are shared
        cleanPolyData = vtkCleanPolyData()
        cleanPolyData.SetInputData(PolyData)
        
        # Use a filter to smooth the data
        smooth_loop = vtkLoopSubdivisionFilter()
        smooth_loop.SetNumberOfSubdivisions(3)
        smooth_loop.SetInputConnection(cleanPolyData.GetOutputPort())
        return smooth_loop
        
    @staticmethod
    def get_line_actor(smooth_loop, chassis_cg):
        return get_spline_actor(smooth_loop, chassis_cg)

    @staticmethod
    def get_surface_actor(smooth_loop):
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
