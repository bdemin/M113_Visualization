import random
import numpy as np


def get_soil_type_arr(path = None):
    if path:
        pass
    else:
        soil_map = np.zeros((m,n), dtype=int)
        choices = (1,2,3,4,5,6)
        # for i in range(m):
            # for j in range(n):
                # soil_map[i,j] = random.choice(choices)
        soil_map[:, int(n/2):-1] = 1
        soil_map[int(m/2):-1, :] = 2
        soil_map[40:44, 40:44] = 3
        soil_map[0:3, 0:3] = 4
        soil_map[0:3, -4:-1] = 5