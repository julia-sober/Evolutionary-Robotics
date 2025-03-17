from solution import SOLUTION
import constants as c
import copy

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(0, c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        for key in self.parents:
            self.parents[key].Evaluate(directOrGUI="GUI")
        # for currentGeneration in range(c.numberOfGenerations):
        #     self.Evolve_For_One_Generation()
        pass
        
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate(directOrGUI="DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = copy.deepcopy(self.child)

    def Print(self):
        print()
        print()
        print(f"Parent's fitness: {self.parent.fitness}, Child's fitness: {self.child.fitness}")
        print()

    def Show_Best(self):
        # self.parent.Evaluate(directOrGUI="GUI")
        pass