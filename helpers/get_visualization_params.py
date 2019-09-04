def m113_novid():
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

    visualization_params = {
        'vehicle_type': vehicle_type,
        'parent_directory': parent_directory,
        'bodies': bodies,
        'surface': surface,
        'video': video
    }

    return visualization_params
