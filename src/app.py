import numpy as np

from helpers.get_latest_directory import get_latest_directory
import bodies.vehicle

from surface.classes import Surface

from visualization.visualizer import Visualizer


class VisualizeDBDSimulation(object):
    def __init__(self, visualization_params):
        self.params = visualization_params
        self.path = get_latest_directory(visualization_params['parent_directory'])

    def load_bodies_data(self):
        # Need to add bodies param
        invoke_vehicle_method = getattr(bodies.vehicle, self.params['vehicle_type'])
        self.vehicle = invoke_vehicle_method(self.path)

    def load_surface_data(self, surface_xyz_data = None):
        self.surface = Surface(self.path, surface_xyz_data, self.params['surface'], self.vehicle.data['chassis'][0].path_loc)

    def load_visualization(self):
        total_time = np.loadtxt(self.path + 'Time_Data.txt', delimiter = ',')
        num_frames = self.vehicle.data['chassis'][0].path_dir.shape[0]

        visualizer = Visualizer(self.params['video'], self.vehicle, self.surface)
        visualizer.add_actors()
        visualizer.init_callback(total_time, num_frames)
        