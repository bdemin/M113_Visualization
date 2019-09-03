import numpy as np

from helpers.get_latest_directory import get_latest_directory
import bodies.vehicle

from surface.classes import Surface

from visualization.visualizer import Visualizer

# from simulation_description import show_description


class VisualizeDBDSimulation(object):
    def __init__(self, visualization_params):
        self.params = visualization_params
        self.path = get_latest_directory(visualization_params['parent_directory'])


    def load_bodies_data(self):
        # Need to add bodies param
        invoke_vehicle_method = getattr(bodies.vehicle, self.params['vehicle_type'])
        self.vehicle = invoke_vehicle_method(self.path)


    def load_surface_data(self):
        self.surface = Surface(self.path, None, self.params['surface'], self.vehicle.bodies['Chassis'][0].path_loc)
    

    def load_visualization(self):
        total_time = np.loadtxt(self.path + 'Time_Data.txt', delimiter = ',')
        num_frames = self.vehicle.bodies['Chassis'][0].path_dir.shape[0]

        visualizer = Visualizer(self.params['video'])
        visualizer.add_actors(self.vehicle.bodies, self.surface)
        visualizer.init_callback(self.vehicle.bodies, total_time, num_frames)
        