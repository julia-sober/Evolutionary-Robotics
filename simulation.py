from world import WORLD
from robot import ROBOT

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim

class SIMULATION:
    
    def __init__(self):
        simulation = SIMULATION()
        self.world = WORLD()
        self.robot = ROBOT()

        self.physicsClient = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        pyrosim.Prepare_To_Simulate(robotId)