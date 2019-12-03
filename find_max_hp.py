import numpy as np


folder = 'C:/Users/bdemin/Dropbox/Work/Tests - 27.11.2019/Turning/TurningRadius_0Deg/'

data = np.loadtxt(folder + 'HP.txt')
print(np.max(data))
