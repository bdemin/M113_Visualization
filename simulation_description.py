def show_description(path):
    if '1' in path:
        print('Simulation_1: Straight line drive on a wavey 2D surface')
    if '2' in path:
        print('Simulation_2: Left turn drive on a wavey 2D surface')    
    if '3' in path:
        print('Simulation_3: Straight line drive on a two phase-shifted 2D surfaces')
    if '4' in path:
        print('Simulation_4: Straight line drive on a complex 3D surface (slow)')      
    if '5' in path:
        print('Simulation_5: Complex path drive on a simplified 3D surface')
    if '6' in path:
        print('Simulation_6: Straight line drive on a wavey surface with obstacles (sphere based)')
    if '7' in path:
        print('Simulation_7: Straight line drive on a wavey surface with obstacles (STL based)')