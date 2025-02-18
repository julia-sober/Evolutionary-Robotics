# import numpy as np
import pybullet as p
# import pybullet_data
# import pyrosim.pyrosim as pyrosim
# import time
# import constants as c

from simulation import SIMULATION

# simulation = SIMULATION()


# robotId = p.loadURDF("body.urdf")


# backLegSensorValues = np.zeros(1000)
# frontLegSensorValues = np.zeros(1000)

# x = np.linspace(0, 2*np.pi, 1000)
# targetAnglesBackLeg = c.amplitudeBackLeg * np.sin(c.frequencyBackLeg * x + c.phaseOffsetBackLeg)
# np.save("data/targetAnglesBackLeg.npy", targetAnglesBackLeg)
# targetAnglesFrontLeg = c.amplitudeFrontLeg * np.sin(c.frequencyFrontLeg * x + c.phaseOffsetFrontLeg)
# np.save("data/targetAnglesFrontLeg.npy", targetAnglesFrontLeg)

# for i in range(1000):
#     p.stepSimulation()
#     backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
#     pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_BackLeg", controlMode = p.POSITION_CONTROL,
#                                 targetPosition = targetAnglesBackLeg[i], maxForce = 20)
#     frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
#     pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_FrontLeg", controlMode = p.POSITION_CONTROL,
#                                 targetPosition = targetAnglesFrontLeg[i], maxForce = 20)
#     time.sleep(1/60)
#     # print(f"Iteration {i+1}")

# p.disconnect()

# np.save("data/backLegSensorData.npy", backLegSensorValues)
# np.save("data/frontLegSensorData.npy", frontLegSensorValues)