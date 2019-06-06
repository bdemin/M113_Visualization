import numpy as np


def Create_Ground():
    size_x = 354, size_y = 763
    max_r = 12, min_r = 1

    GroundSurf = np.zeros((size_x, size_y))
    num_spheres = 10000
    for i in range(num_spheres):
        x0 = round(size_x * rand)
        y0 = round(size_y * rand)
        rand_rad = (max_r - min_r) * rand
        for x1 in range(x0 - round(rand_rad), x0 + round(rand_rad)):
            for y1 in range(y0 - round(rand_rad), y0 + round(rand_rad)):
                if x1>0 and x1<size_x and y1>0 and y1<size_y:
                    z_add = rand_rad**2 - ((x1-x0)**2 + (y1-y0)**2)
                    if z_add > 0:
                        GroundSurf[x1,y1] = GroundSurf[x1,y1] + z_add

    z_max = max(GroundSurf)
    z_min = min(GroundSurf)
    scale_factor = 1.1
    for i in range(size_x):
        for j in range(size_y):
            GroundSurf[i,j] = ((GroundSurf[i,j] - z_min)/(z_max - z_min))*scale_factor - 1

    GroundSurf[:,0] = np.arange(-20, -20 + 353*0.2, 0.2)
    GroundSurf[0,:] = np.arange(-20, -20 + 353*0.2, 0.2)
    GroundSurf[:,0] = -20:0.2:-20+353*0.2
    GroundSurf[0,:] = -30:0.2:-30+762*0.2


surface = Surface(path_directory)
