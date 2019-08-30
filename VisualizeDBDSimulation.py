import numpy as np

from helpers.get_latest_directory import get_latest_directory
import bodies.vehicle

from surface.classes import Surface

# from graphics.visualize2 import visualize

# from simulation_description import show_description


class VisualizeDBDSimulation(object):
    def __init__(self, visualization_params):
        self.params = visualization_params
        self.path = get_latest_directory(visualization_params['parent_directory'])
        self.total_time = np.loadtxt(self.path + 'Time_Data.txt', delimiter = ',')


    def load_bodies_data(self):
        invoke_vehicle_method = getattr(bodies.vehicle, self.params['vehicle_type'])
        self.bodies = invoke_vehicle_method(self.path)


    def load_surface_data(self):
        self.surface = Surface()
