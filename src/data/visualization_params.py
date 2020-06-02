class SimulationTypes(object):
    # Class for holding various sets of simulation parameters

    def m113_novid(self):
        # M113 visualization with all bodies, surface and no video recording

        parent_directory = '../M113_tests/Data_Movies/'

        vehicle_type = 'M113'

        bodies = {
            'Chassis': True,
            'road_wheels': True,
            'trailing_arms': True,
            'sprockets': True,
            'idlers': True,
            'track_units': True
        }

        surface = {
            'visualize_surface': True,
            'soil_map_flag': True,
            'color_map_flag': False,
            'path_spline_flag': True
        }

        video = {
            'record_video_flag': False,
        }

        self.params = {
            'vehicle_type': vehicle_type,
            'parent_directory': parent_directory,
            'bodies': bodies,
            'surface': surface,
            'video': video
        }

    def m113_vid(self):
        # M113 visualization with all bodies, surface and video recording

        parent_directory = '../M113_tests/Data_Movies/'

        vehicle_type = 'M113'

        bodies = {
            'Chassis': True,
            'road_wheels': True,
            'trailing_arms': True,
            'sprockets': True,
            'idlers': True,
            'track_units': True
        }

        surface = {
            'visualize_surface': True,
            'soil_map_flag': True,
            'color_map_flag': False,
            'path_spline_flag': True
        }

        video = {
            'record_video_flag': True,
        }

        self.params = {
            'vehicle_type': vehicle_type,
            'parent_directory': parent_directory,
            'bodies': bodies,
            'surface': surface,
            'video': video
        }
        
    def eitan_novid(self):
        # Eitan visualization with all bodies, surface and no video recording

        parent_directory = '../Eitan/Results/'

        vehicle_type = 'Eitan'

        bodies = {
            'Chassis': True,
            'road_wheels': True,
        }

        surface = {
            'visualize_surface': True,
            'soil_map_flag': False,
            'color_map_flag': False,
            'path_spline_flag': False,
            'texture_map': 'grass'
        }

        video = {
            'record_video_flag': False,
        }

        self.params = {
            'vehicle_type': vehicle_type,
            'parent_directory': parent_directory,
            'bodies': bodies,
            'surface': surface,
            'video': video
        }

class VisualizationParameters(SimulationTypes):
    # Class that deals with various visualization parameters - which bodies to include, surface filters, video recording, etc.

    def load_data(self, method_string):
        # Load simulation data into instance
        
        invoke_method = getattr(self, method_string)
        invoke_method()

    @property
    def get_data(self):
        # Return all parameters regarding the visualization
        return self.params

params = VisualizationParameters()
