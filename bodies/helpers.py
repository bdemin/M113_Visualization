import numpy as np

from bodies.classes import Body


def create_bodies(path_directory, type_, side = None):
    bodies = []
    path_data = np.loadtxt(path_directory + type_ + '.txt', delimiter = ',')
    num_cols = path_data.shape[1]
    for index in range(0, num_cols, 6):
        loc_slice = slice(index, index+3)
        dir_slice = slice(index+3, index+6)
        path_loc = np.copy(path_data[:, loc_slice])
        path_dir = np.copy(path_data[:, dir_slice])
        if side:
            if index < num_cols/2:
                side = 'L'
                path_dir[:,2] = path_dir[:,2] - np.pi
                path_dir[:,0] = -path_dir[:,0]
            else:
                side = 'R'
        bodies.append(Body(type_, path_loc, path_dir, side))    
    return bodies


def find_angle(x0, y0):
    return np.arctan(y0/x0)*180/np.pi+90