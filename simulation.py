from world import WORLD
from robot import ROBOT

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time

class SIMULATION:
    
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for timeStep in range(1000):
            p.stepSimulation()
            self.robot.Sense(timeStep)
            self.robot.Think(timeStep)
            self.robot.Act(timeStep)
            time.sleep(1/60)

    def __del__(self):
        p.disconnect()     