from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np

class PARALLEL_HILL_CLIMBER:

    def __init__(self, testVariant):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.testVariant = testVariant
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(0, c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID, self.testVariant)
            self.nextAvailableID += 1
        self.fitnessVals = np.zeros((c.populationSize, c.numberOfGenerations))

    def Evolve(self):
        self.Evaluate(self.parents, 0)
        for currentGeneration in range(1, c.numberOfGenerations):
            self.Evolve_For_One_Generation(currentGeneration)
        np.save("data/fitness_values_" + self.testVariant + ".npy", self.fitnessVals)
        
    def Evolve_For_One_Generation(self, currentGeneration):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children, currentGeneration)
        # self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for key in self.children:
            self.children[key].Mutate()

    def Select(self):
        for key in self.parents:
            if self.parents[key].fitness < self.children[key].fitness:
                self.parents[key] = copy.deepcopy(self.children[key])

    def Evaluate(self, solutions, currentGeneration):
        for key in solutions:
            solutions[key].Start_Simulation("DIRECT")
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()
            self.fitnessVals[key, currentGeneration] = solutions[key].fitness

    def Print(self):
        print()
        print()
        for key in self.parents:
            print()
            print(f"Parent's fitness: {self.parents[key].fitness}, Child's fitness: {self.children[key].fitness}")
            print()
        print()

    def Show_Best(self):
        bestFitness = 0
        bestParent = self.parents[0]
        for key in self.parents:
            if self.parents[key].fitness > bestFitness:
                bestFitness = self.parents[key].fitness
                bestParent = self.parents[key]
        bestParent.Start_Simulation("GUI")
        print(bestFitness)
