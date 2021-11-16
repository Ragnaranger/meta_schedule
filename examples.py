import numpy as np
from schedule import Schedule, Teacher, Group
import pyswarms as ps
import time

def example1():

    s = Schedule(1, 4)
    s.add_teacher(Teacher('Daniel',   set(), np.array([0, 0, 0, 0])))
    s.add_teacher(Teacher('Henrique', set(), np.array([0, 1, 1, 1])))
    s.add_teacher(Teacher('Luiz',     set(), np.array([1, 0, 1, 1])))
    s.add_teacher(Teacher('Gustavo',  set(), np.array([1, 1, 0, 1])))


    # s.add_teacher(Teacher('Inutil',  set(), np.array ([0, 0, 0, 0])))
    # s.add_teacher(Teacher('Ocupado',  set(), np.array([1, 1, 1, 1])))
    

    s.add_group(Group('Primeiro ano', {'Daniel':1, 'Henrique':1, 'Luiz':1, 'Gustavo':1}))
    s.add_group(Group('Segundo ano', {'Daniel':2}))
    

    # n_particles precisa ser múltiplo de n_threads
    n_particles = 40
    n_threads = 8
    s.compile(n_particles, n_threads)

    # Para visualizar as matrizes de requerimentos, usadas na função evaluate
    # print(s.all_group_requirements)       # (prof, group)
    # print(s.all_group_requirements.shape) # (4, 2)
    # print(s.all_restrictions)             # (prof, dia/hr)
    # print(s.all_restrictions.shape)       # (4, 4)


    x = np.array(
    # [prof : dias/horarios : grupos]
    # shape: [4, 4, 2]

    # Daniel
    #  G1  G2
    [[[0., 1.], # d1h1
      [0., 1.], # d1h2
      [0., 0.], # d1h3
      [1., 0.]],# d1h4

    # Henrique
     [[1., 0.], 
      [0., 0.],
      [0., 0.],
      [0., 0.]],

    # Luiz
     [[0., 0.], 
      [1., 0.],
      [0., 0.],
      [0., 0.]],
      
    # Gustavo
     [[0., 0.], 
      [0., 0.],
      [1., 0.],
      [0., 0.]]]
    )

    # print(x[:,:, 0])
    # print(x.shape)
    # x = x.reshape(1, -1)
    # print(s.evaluate(x))
    # input()


    options = {'c1': 1000.0, 'c2': 0.3, 'w':0.9, 'k':2, 'p':1}

    start = time.time()
    optmizer = ps.discrete.BinaryPSO(n_particles, s.dimensions, options=options)
    cost, pos = optmizer.optimize(s.evaluate, iters=1000, n_processes=n_threads)
    # print('Cost: ', cost,'Pos: ', pos)
    # print(pos.reshape(s.shape))
    stop = time.time()
    print('Duration: ', stop-start)


if __name__ == '__main__':

    example1()