from sensor import SENSOR
from motor import MOTOR

import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np

class ROBOT:
    
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        ROBOT.Prepare_To_Sense(self)
        ROBOT.Prepare_To_Act(self)

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            values = np.zeros(1000)
            self.sensors[linkName] = SENSOR(linkName, values)

    def Sense(self, timeStep):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(timeStep)

    def Prepare_To_Act(self):
        self.motors = {}
        self.amplitude = np.pi/4.0
        self.frequency = 30
        self.offset = 0
        for jointName in pyrosim.jointNamesToIndices:
            if jointName == "Torso_FrontLeg":
                frequency = self.frequency/2
            else:
                frequency = self.frequency
            x = np.linspace(0, 2*np.pi, 1000)
            targetAngles = self.amplitude* np.sin(frequency * x + self.offset)
            self.motors[jointName] = MOTOR(jointName, targetAngles)

    def Act(self, timeStep):
        for jointName in self.motors:
            self.motors[jointName].Set_Value(self.robotId, timeStep)
            
        
    