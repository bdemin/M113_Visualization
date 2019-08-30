def m113_novid():
    # M113 visualization with all bodies, surface and no video recording

    parent_directory = '../M113_tests/Data_Movies/'

    vehicle_type = 'M113'

    logic = {
        'record_video_flag': False,
        'visualize_surface': True,
        'soil_map_flag': True,
    }

    bodies = {
        'Chassis': True,
        'road_wheels': True,
        'trailing_arms': True,
        'sprockets': True,
        'idlers': True,
        'track_units': True
    }

    visualization_params = {
        'vehicle_type': vehicle_type,
        'parent_directory': parent_directory,
        'logic': logic,
        'bodies': bodies,
    }

    return visualization_params
