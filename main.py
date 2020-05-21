from data.visualization_params import params
from visualizer_app import app


def main():
    params.load_data('m113_novid')

    app.load_params(params.get_data)
    app.load_bodies_data()
    app.load_surface_data()
    app.load_visualization()

if __name__ == '__main__':
    main()
