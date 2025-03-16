from world import WORLD
from robot import ROBOT

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import constants as c

class SIMULATION:
    
    def __init__(self, directOrGUI):
        self.directOrGUI = directOrGUI
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for timeStep in range(c.numTimeSteps):
            p.stepSimulation()
            self.robot.Sense(timeStep)
            self.robot.Think(timeStep)
            self.robot.Act(timeStep)
            if self.directOrGUI == "GUI":
                time.sleep(1/120)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()     