from sensor import SENSOR
from motor import MOTOR

import pybullet as p
import numpy as np
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import time


class ROBOT:
    
    def __init__(self, solutionID):
        urdf_path = os.path.join(os.path.dirname(__file__), "body.urdf")
        try:
            self.robotId = p.loadURDF(urdf_path)
            print()
            print(f"ROBOTID = {self.robotId}!!!!!!!!!!")
            print()
            self.error = False
            self.solutionID = solutionID
            self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
            self.sensorVals = np.zeros((c.numTimeSteps, 9))
            self.zPositions = np.zeros(c.numTimeSteps)
            os.system("rm " + "brain" + str(solutionID) + ".nndf")
            pyrosim.Prepare_To_Simulate(self.robotId)
            ROBOT.Prepare_To_Sense(self)
        except Exception as e:
            print(f"Error in simulation: {e}")
            self.robotId = np.nan
            self.error = True
            self.solutionID = solutionID
            self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
            self.sensorVals = np.zeros((c.numTimeSteps, 9))
            self.zPositions = np.zeros(c.numTimeSteps)
            os.system("rm " + "brain" + str(solutionID) + ".nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            values = np.zeros(c.numTimeSteps)
            self.sensors[linkName] = SENSOR(linkName, values)

    def Sense(self, timeStep):
        ctr = 0
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(timeStep)
            self.sensorVals[timeStep][ctr] = self.sensors[linkName].values[timeStep]
            ctr += 1
        print(f"Sensing at timestep {timeStep}")

    def Act(self, timeStep):
        print("Acting...")
        self.motors = {}
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName] = MOTOR(jointName)
                delay = 0
                if "LowerLeg" in jointName:
                    delay = 0 
                elif "Torso" in jointName:
                    delay = 0 
                if timeStep >= delay:
                    angleScale = c.torsoMotorJointRange if "Torso" in jointName else c.legMotorJointRange
                    self.motors[jointName] = MOTOR(jointName)
                    self.motors[jointName].Set_Value(self.robotId, desiredAngle * angleScale)
                
    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Record_Position(self, timeStep):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        zPosition = basePosition[2]
        self.zPositions[timeStep] = zPosition

    def Get_Fitness(self, simulationError):        
        bestJumpDuration = 0
        currentStreak = 0
        streakStart = None

        for t, row in enumerate(self.sensorVals):
            if row.sum() == len(row) * -1:
                if currentStreak == 0:
                    streakStart = t
                currentStreak += 1
            else:
                if currentStreak > 0 and streakStart is not None:
                    streakEnd = t
                    if currentStreak > bestJumpDuration:
                        bestJumpDuration = currentStreak

                currentStreak = 0
                streakStart = None

        if currentStreak > 0 and streakStart is not None:
            streakEnd = len(self.sensorVals)
            if currentStreak > bestJumpDuration:
                bestJumpDuration = currentStreak

        if self.error or simulationError:
            fitness = np.nan
        else:
            fitness = bestJumpDuration**(1/2)
            # fitness = max(self.zPositions)
            # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
            # basePosition = basePositionAndOrientation[0]
            # fitness = basePosition[0]

        f = open("tmp" + str(self.solutionID) + ".txt", "w")
        f.write(str(fitness))
        f.close()
        time.sleep(0.1)
        os.rename("tmp" + str(self.solutionID) + ".txt", "fitness" + str(self.solutionID) + ".txt")      
        
    