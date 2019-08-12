from helpers.functions import get_directory
from simulation_description import show_description
from bodies.vehicle import M113


class DBDSimulation(object):
    def __init__(self, vehicle_type, record_video, soil):
        self.vehicle_type = vehicle_type
        self.record_video = record_video
        self.soil = soil

        method_to_call = getattr(DBDSimulation, self.vehicle_type)
        simulation = method_to_call(self)

        show_description(self.path)

        self.bodies = build_visualization_data(self.path, self.vehicle_type)


    def m113(self):
        parent_directory = '../M113_tests/Data_Movies/'
        self.path = get_directory(parent_directory)
        sim = M113(self.path)
        # def build_visualization_data(path, vehicle_type):
        #     # Create bodies
        #     path = path + '/' + vehicle_type
        #     data = []
        #     if vehicle_type == 'm113':
                # road_wheels = create_bodies(path, 'Road_Wheel', side = True)
                # trailing_arms = create_bodies(path, 'Trailing_Arm', side = True)
                # sprockets = create_bodies(path, 'Sprocket', side = True)
                # idlers = create_bodies(path, 'Idler', side = True)
                # track_units = create_bodies(path, 'Track_Unit')

            # else:
                # return None

        

    def eitan(self):
        parent_directory = '../M113_tests/Data_Movies/'
        self.path = get_directory(parent_directory)
