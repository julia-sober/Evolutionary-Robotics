import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
    
    def __init__(self, jointName, targetAngles):
        self.jointName = jointName
        self.targetAngles = targetAngles

    def Set_Value(self, robot, timeStep):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robot, jointName=self.jointName, controlMode=p.POSITION_CONTROL,
                                    targetPosition=self.targetAngles[timeStep], maxForce=20)
        
    def Save_Values(self):
        filename = "data/" + self.jointName + "MotorData.npy"
        np.save(filename, self.targetAngles)
    