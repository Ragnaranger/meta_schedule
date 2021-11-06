import numpy as np

# Import PySwarms
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx



def evaluate(x:np.ndarray) -> np.ndarray:
    y = np.array([1, 2, 3, 4, 5])
    return np.sum(np.abs(x-y), axis=1)

def evaluate_bin(x:np.ndarray) -> np.ndarray:
    return np.sum(1000 - (x+3) * np.array([1, 2, 3, 4, 5]),axis=1)

if __name__ == '__main__':
    # help(fx)


    options = {'c1': 0.5, 'c2': 0.3, 'w':0.9, 'k':2, 'p':1}

    # optmizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=5, options=options)
    optmizer = ps.discrete.BinaryPSO(50, 5, options=options)
    cost, pos = optmizer.optimize(evaluate_bin, iters=10000)
    print('Cost: ', cost,'Pos: ', pos)

    # b = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    # a = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
    # print(evaluate_bin(b))
    # print(a*b)
