from schedule import Schedule, Teacher, Group
import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm

from numpy.core.numeric import Inf

def random_optimizer(function, n_particles, iterations, n_dimensions, proportion_one=0.5):

    global_min = float(Inf)
    
    min_history = []

    for _ in tqdm(range(iterations)):
        particles = np.random.choice([0, 1], (n_particles, n_dimensions), p=[1-proportion_one, proportion_one])
        result = function(particles)

        pos_local_min = np.argmin(result)
        local_min = result[pos_local_min]

        if local_min < global_min:
            global_min = local_min
            best_sollution = particles[pos_local_min, :]

        min_history.append(global_min)

    return global_min, best_sollution, min_history

def plot_cost_hist(cost_hist):
    fig, ax = plt.subplots()
    ax.plot(range(len(cost_hist)), cost_hist)

    ax.set(xlabel='iterations', ylabel='cost',
       title='Cost History')
    # plt.show()
    


def example(iterations=50000, proportion_one=0.5, auto_proportion=False):
    s = Schedule(5, 4)
    s.add_teacher(Teacher('Daniel',   set(), np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])))
    s.add_teacher(Teacher('Henrique', set(), np.array([0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1])))
    s.add_teacher(Teacher('Luiz',     set(), np.array([1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1])))
    s.add_teacher(Teacher('Gustavo',  set(), np.array([1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1])))


    s.add_teacher(Teacher('Inutil',  set(), np.array ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])))
    s.add_teacher(Teacher('Ocupado',  set(), np.array([1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1])))
    

    s.add_group(Group('Primeiro ano', {'Daniel':1, 'Henrique':1, 'Luiz':1, 'Gustavo':1}))
    s.add_group(Group('Segundo ano', {'Daniel':1, 'Henrique':1, 'Ocupado':1}))
    s.add_group(Group('Terceiro ano', {'Henrique':1, 'Luiz':1}))
    s.add_group(Group('Quarto ano', {'Inutil':1, 'Ocupado':1, 'Daniel':1}))

    # n_particles precisa ser múltiplo de n_threads
    n_particles = 40
    n_threads = 1
    s.compile(n_particles, n_threads)


    if auto_proportion:
        n_classes = 0
        for group in s.list_of_groups:
            group:Group
            n_classes += sum(group.diciplines.values())
        
        total = s.shape[0] * s.shape[1] * s.shape[2]

        proportion_one = n_classes/total
        print('Auto-proportion: ', proportion_one)



    start = time.time()
    cost, pos, cost_hist = random_optimizer(s.evaluate, n_particles, iterations, s.dimensions, proportion_one)
    stop = time.time()
    print('Duration: ', stop-start)

    # print('Cost: ', cost,'Pos: ', pos)
    # print(pos.reshape(s.shape))
    print('Melhor custo: ', cost)
    plot_cost_hist(cost_hist)


if __name__ == '__main__':

    example()

    example(proportion_one=0.1)

    example(proportion_one=0.05)

    example(auto_proportion=True)

    plt.show()
