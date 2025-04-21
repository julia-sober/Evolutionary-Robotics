from world import WORLD
from robot import ROBOT

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import constants as c
import os

class SIMULATION:
    
    def __init__(self, directOrGUI, solutionID):
        print(f"SIMULATION init called with {directOrGUI} {solutionID}")
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setGravity(0, 0, -9.8)
        # p.setPhysicsEngineParameter(enableFileCaching=0)
        # p.setPhysicsEngineParameter(deterministicOverlappingPairs=1)
        # p.setPhysicsEngineParameter(numSolverIterations=150)
        # p.setPhysicsEngineParameter(contactBreakingThreshold=0.001)

        try:
            self.robot = ROBOT(self.solutionID)
            self.world = WORLD()
            self.error = False
        
        except Exception as e:
            print(f"Simulation failed: {e}")
            self.error = True

    def Run(self):
        if not self.error and not self.robot.error:
            max_steps = c.numTimeSteps * 2 
            for timeStep in range(c.numTimeSteps):
                print("Timestep:", timeStep)
                if timeStep > max_steps:
                    print("Timeout reached, breaking out of simulation loop.")
                    break
                p.stepSimulation()
                self.robot.Sense(timeStep)
                self.robot.Think()
                self.robot.Record_Position(timeStep)
                self.robot.Act()
                if self.directOrGUI == "GUI":
                    time.sleep(c.sleepSize)

    def Get_Fitness(self):
        self.robot.Get_Fitness(self.error)
        exit()

    def __del__(self):
        p.disconnect()   