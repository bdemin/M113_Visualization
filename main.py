from DBDSimulation import DBDSimulation


def main():
    vehicle_type = 'm113'
    record_video = False
    soil = True

    simulation = DBDSimulation(vehicle_type, record_video, soil)

if __name__ == '__main__':
    main()