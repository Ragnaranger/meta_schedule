import numpy as np
import pyswarms as ps


class Teacher:
    def __init__(self, name:str, diciplines:set, array_of_restrictions:np.ndarray):
        self.list_of_constraints = []
        self.name = name

        # Disciplinas não serão implementadas agora, por enquanto, se um professor
        #  leciona mais de uma disciplina, basta adicionar ele mais de uma vez, com um nome diferente
        #  Sim, pode acontecer dele cair em horários conflitantes... (shhhhhhh...)
        self.diciplines = diciplines

        # O vetor de restrições vem no seguinte formato
        # O tamanho do vetor é o número de horários de cada dia * a quantidade de dias
        # [dia1_horario1, dia1_horario2, dia1_horario3, dia2_horario1, ...]
        # 0 é horário livre, 1 é horário proibido
        self.restrictions = array_of_restrictions

class Group:
    # O dict é no formato {disciplina:quantidade_de_aulas_necessárias}
    def __init__(self, name:str, diciplines:dict):
        self.name = name

        # Por enquanto, disciplinas tem como chave o nome do professor
        self.diciplines = diciplines


class Schedule:
    def __init__(self, n_days_in_week=5, n_classes_per_day=4):
        self.n_days_in_week = n_days_in_week
        self.n_classes_per_day = n_classes_per_day

        self.dimensions = 0

        self.list_of_teachers = []

        # Implementar turmas
        self.list_of_groups = []


    # Compila o schedule para prepará-lo para otimização
    # Aqui, algumas variáveis são preparadas para acelerar o processo de avaliação de horários
    # Exemplo, uma matriz com a disponibilidade de professores é montada para que todos sejam comparados
    #  de uma vez
    def compile(self, n_particles):
        # Quantidade de dimensões necessárias para o PSO
        self.dimensions = len(self.list_of_groups) * len(self.list_of_teachers) * self.n_days_in_week * self.n_classes_per_day
        self.shape = [len(self.list_of_teachers), self.n_days_in_week * self.n_classes_per_day, len(self.list_of_groups)]

        # Esse shape inclui a quantidade de partículas
        self.shape_evaluate = [n_particles, len(self.list_of_teachers), self.n_days_in_week * self.n_classes_per_day, len(self.list_of_groups)]


        # Criando uma matriz com as restrições de cada professor
        all_restrictions = []
        for teacher in self.list_of_teachers:
            teacher:Teacher
            all_restrictions.append(teacher.restrictions)

        self.all_restrictions = np.array(all_restrictions)




        # Criando uma matriz com a necessidade de aulas de cada grupo
        all_group_requirements = []
        # Para cada grupo
        for group in self.list_of_groups:
            group:Group
            single_group_requirements = []

            # Verificar se existe uma necessidade com cada professor
            for teacher in self.list_of_teachers:

                # Se estiver na lista de necessidades, adicionar a quantidade especificada
                if teacher.name in group.diciplines:
                    single_group_requirements.append(group.diciplines[teacher.name])
                
                # Se não, adicionar 0
                else:
                    single_group_requirements.append(0)

                
            all_group_requirements.append(single_group_requirements)
        self.all_group_requirements = np.array(all_group_requirements).T


    def evaluate(self, x:np.ndarray):
        # Coeficiente de horário disponível de professor
        COEF_PROF_HR = 20

        # Coeficiente de aulas que grupo deixou de receber
        COEF_GROUP_CLASS_MISSING = 20

        # Coeficiente de aulas que grupo recebeu a mais
        COEF_GROUP_CLASS_EXTRA = 20

        # Coeficiente professor dando mais de 1 aula por horário
        COEF_PROF_OVERLAP_TIME = 20

        # Coeficiente grupo recebendo mais de 1 aula por horário
        COEF_GROUP_OVERLAP_TIME = 20
        
        x = x.reshape(self.shape_evaluate)
        n_particles = self.shape_evaluate[0]
        points = np.zeros(self.shape_evaluate[0])

        # Verificar se prof estão em horários disponíveis
        prof_hora = np.sum(x, axis=3) # axis=grupo
        points += np.sum((prof_hora * self.all_restrictions).reshape(n_particles, -1), axis=1 ) * COEF_PROF_HR
                


        # Verificar se grupos tem as aulas que precisam
        group_aula = np.sum(x, axis=2) # axis=horario

        classes = group_aula - self.all_group_requirements
        classes = np.where(classes < 0, # Os negativos são classes faltando
                    classes * -COEF_GROUP_CLASS_MISSING, # Quando faltam aulas
                    classes * COEF_GROUP_CLASS_EXTRA) # Quando sobram aulas

        points += np.sum(classes.reshape(n_particles, -1), axis=1)




        # Verificar se professores tem horários conflitantes
        #particle:prof:hr:turma
        points += np.count_nonzero(np.sum(x, axis=(3)) > 1, axis=(1, 2)) * COEF_PROF_OVERLAP_TIME
        

        # Verificar se grupos tem horários conflitantes
        points += np.count_nonzero(np.sum(x, axis=(1)) > 1, axis=(1, 2)) * COEF_PROF_OVERLAP_TIME
        return points

    def codify():
        pass

    
    def decodify(self, x:np.ndarray):
        # professor:dia/horario:turma
        return x.reshape(self.shape)


    def add_teacher(self, teacher:Teacher):
        self.list_of_teachers.append(teacher)
    
    def add_group(self, group:Group):
        self.list_of_groups.append(group)


# def func(x):
#     return x[0]*2 + x[1]

def test():
    # a = np.zeros([3, 6, 4])[0] # professor 0
    # a[0, 0] = 1
    # a[2, 0] = 1
    # a[5, 0] = 1
    # print(a)

    # b = np.array([1, 0, 1, 0, 1, 0])
    
    # print('b\n', b)

    # c= np.sum(a, axis=1)
    # print('c\n', c)

    # print('sum\n', np.sum(c*b))


    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.array([1, 2, 3])
    print(a+b)

def example():

    s = Schedule(1, 4)
    s.add_teacher(Teacher('Daniel',   set(), np.array([0, 0, 0, 0])))
    s.add_teacher(Teacher('Henrique', set(), np.array([0, 1, 1, 1])))
    s.add_teacher(Teacher('Luiz',     set(), np.array([1, 0, 1, 1])))
    s.add_teacher(Teacher('Gustavo',  set(), np.array([1, 1, 0, 1])))

    # s.add_teacher(Teacher('Inutil',  set(), np.array([0, 0, 0, 0])))
    # s.add_teacher(Teacher('Ocupado',  set(), np.array([1, 1, 1, 1])))
    

    s.add_group(Group('Primeiro ano', {'Daniel':1, 'Henrique':1, 'Luiz':1, 'Gustavo':1}))
    s.add_group(Group('Segundo ano', {'Daniel':1}))

    n_particles = 50
    s.compile(n_particles=n_particles)

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
      [0., 0.], # d1h2
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
    x = x.reshape(1, -1)
    # s.evaluate(x)


    options = {'c1': 0.5, 'c2': 0.3, 'w':0.9, 'k':2, 'p':1}
    optmizer = ps.discrete.BinaryPSO(n_particles, s.dimensions, options=options)
    cost, pos = optmizer.optimize(s.evaluate, iters=25000)
    print('Cost: ', cost,'Pos: ', pos)
    print(pos.reshape(s.shape))

if __name__ == '__main__':
    # test()
    example()


    # a = np.array([[1, 5], [1, 6], [1, 7]])
    # a.vectorize(print, axis=0)
    # nprint = np.vectorize(func)

    # y = np.apply_along_axis(func, axis=1, arr=a)

    # print(y)
