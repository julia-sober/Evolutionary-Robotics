import numpy as np
import math
import random
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time

amplitudeBackLeg = np.pi
frequencyBackLeg = 30
phaseOffsetBackLeg = 0

amplitudeFrontLeg = np.pi
frequencyFrontLeg = 15
phaseOffsetFrontLeg = np.pi/2.0

physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.setGravity(0, 0, -9.8)
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)

x = np.linspace(0, 2*np.pi, 1000)
targetAnglesBackLeg = amplitudeBackLeg * np.sin(frequencyBackLeg * x + phaseOffsetBackLeg)
np.save("data/targetAnglesBackLeg.npy", targetAnglesBackLeg)
targetAnglesFrontLeg = amplitudeFrontLeg * np.sin(frequencyFrontLeg * x + phaseOffsetFrontLeg)
np.save("data/targetAnglesFrontLeg.npy", targetAnglesFrontLeg)

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_BackLeg", controlMode = p.POSITION_CONTROL,
                                targetPosition = targetAnglesBackLeg[i], maxForce = 20)
    # pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_BackLeg", controlMode = p.POSITION_CONTROL,
    #                             targetPosition = random.uniform(-math.pi/2.0, math.pi/2.0), maxForce = 500)
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_FrontLeg", controlMode = p.POSITION_CONTROL,
                                targetPosition = targetAnglesFrontLeg[i], maxForce = 20)
    # pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_FrontLeg", controlMode = p.POSITION_CONTROL,
    #                             targetPosition = random.uniform(-math.pi/2.0, math.pi/2.0), maxForce = 500)
    time.sleep(1/60)
    # print(f"Iteration {i+1}")

p.disconnect()

np.save("data/backLegSensorData.npy", backLegSensorValues)
np.save("data/frontLegSensorData.npy", frontLegSensorValues)