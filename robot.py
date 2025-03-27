from sensor import SENSOR
from motor import MOTOR

import pybullet as p
import numpy as np
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:
    
    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.solutionID = solutionID
        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
        os.system("rm " + "brain" + str(solutionID) + ".nndf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        ROBOT.Prepare_To_Sense(self)

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            values = np.zeros(1000)
            self.sensors[linkName] = SENSOR(linkName, values)

    def Sense(self, timeStep):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(timeStep)

    def Act(self, timeStep):
        self.motors = {}
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName] = MOTOR(jointName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle*c.motorJointRange)
                
    def Think(self, timeStep):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        f = open("tmp" + str(self.solutionID) + ".txt", "w")
        f.write(str(xPosition))
        f.close()
        print("Created ", "tmp" + str(self.solutionID) + ".txt")
        os.system("mv " + "tmp" + str(self.solutionID) + ".txt " + "fitness" + str(self.solutionID) + ".txt")
        print("Created ", "fitness" + str(self.solutionID) + ".txt")
            
        
    