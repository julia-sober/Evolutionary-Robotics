from solution import SOLUTION
import constants as c
import copy

class HILLCLIMBER:

    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        self.parent.Evaluate(directOrGUI="GUI")
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate(directOrGUI="DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

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
        self.parent.Evaluate(directOrGUI="GUI")