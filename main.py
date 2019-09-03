from VisualizeDBDSimulation import VisualizeDBDSimulation

from helpers.get_visualization_params import m113_novid


def main():
    visualization_params = m113_novid()
    
    vis = VisualizeDBDSimulation(visualization_params)
    vis.load_bodies_data()
    vis.load_surface_data()
    vis.load_visualization()

if __name__ == '__main__':
    main()
