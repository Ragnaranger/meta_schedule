import numpy as np

class Teacher:
    def __init__(self, name:str, diciplines:set):
        self.list_of_constraints = []
        self.name = name
        self.diciplines = diciplines

class Group:
    # O dict é no formato {disciplina:quantidade_de_aulas_necessárias}
    def __init__(self, name:str, diciplines:dict):
        self.name = name
        self.diciplines = diciplines




class Schedule:
    def __init__(self, n_days_in_week=5, n_classes_per_day=4):
        self.n_days_in_week = n_days_in_week
        self.n_classes_per_day = n_classes_per_day

        self.list_of_teachers = []

        # Implementar grupos
        self.list_of_groups = []
        

    def evaluate(self, x):
        pass

    def codify():
        pass

    
    def decodify():
        pass


    def add_teacher(self, teacher:Teacher):
        self.list_of_teachers.append(teacher)


def func(x):
    return x[0]*2 + x[1]


if __name__ == '__main__':

    s = Schedule(1, 2)
    t = Teacher('Daniel')
    s.add_teacher(t)


    func = s.evaluate

    print(func(2))

    # a = np.array([[1, 5], [1, 6], [1, 7]])
    # a.vectorize(print, axis=0)
    # nprint = np.vectorize(func)

    # y = np.apply_along_axis(func, axis=1, arr=a)

    # print(y)
