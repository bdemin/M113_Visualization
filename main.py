from VisualizeDBDSimulation import VisualizeDBDSimulation

from helpers.get_visualization_params import VisualizationParameters


def main():
    PARAMS = VisualizationParameters()
    PARAMS.load_data('m113_novid')

    # visualization_params = m113_novid()
    
    vis = VisualizeDBDSimulation(PARAMS.get_data())
    vis.load_bodies_data()
    vis.load_surface_data()
    vis.load_visualization()

if __name__ == '__main__':
    main()
