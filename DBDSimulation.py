from helpers.functions import get_directory


class DBDSimulation(object):
    def __init__(self, vehicle_type, record_video, soil):
        self.record_video = record_video
        self.soil = soil

        method_to_call = getattr(DBDSimulation, vehicle_type)
        simulation = method_to_call(self)


    def m113(self):
        parent_directory = '../M113_tests/Data_Movies/'
        self.path = get_directory(parent_directory)
        

    def eitan(self):
        parent_directory = '../M113_tests/Data_Movies/'
        self.path = get_directory(parent_directory)
