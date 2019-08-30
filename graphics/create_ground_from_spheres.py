import numpy as np


def create_ground_from_spheres():
    np.random.seed(1)

    size_x = 301; size_y = 701
    max_r = 10; min_r = 0.4
    ground_surf = np.zeros((size_x, size_y))

    num_spheres = 10000
    for i in range(num_spheres):
        x0 = round(size_x * np.random.rand())
        y0 = round(size_y * np.random.rand())
        rand_rad = (max_r - min_r) * np.random.rand()
        for x1 in range(x0 - round(rand_rad), x0 + round(rand_rad)):
            for y1 in range(y0 - round(rand_rad), y0 + round(rand_rad)):
                if x1>0 and x1<size_x and y1>0 and y1<size_y:
                    z_add = rand_rad**2 - ((x1-x0)**2 + (y1-y0)**2)
                    if z_add > 0:
                        ground_surf[x1,y1] = ground_surf[x1,y1] + z_add

    z_max = np.max(ground_surf)
    z_min = np.min(ground_surf)
    scale_factor = 1
    for i in range(size_x):
        for j in range(size_y):
            ground_surf[i,j] = ((ground_surf[i,j] - z_min)/(z_max - z_min))*scale_factor - 1

    ground_surf[:,0] = np.arange(-20, -20 + size_x*0.2, 0.2)
    ground_surf[0,:] = np.arange(-20, -20 + size_y*0.2, 0.2)
    
    size = 101
    return ground_surf[:size,0], ground_surf[0,:size], ground_surf[1:size,1:size]