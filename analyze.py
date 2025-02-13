import numpy as np
import matplotlib.pyplot as plt

targetAnglesBackLeg = np.load("data/targetAnglesBackLeg.npy")
targetAnglesFrontLeg = np.load("data/targetAnglesFrontLeg.npy")

plt.plot(targetAnglesBackLeg, label='targetAnglesBackLeg', linewidth=5)
plt.plot(targetAnglesFrontLeg, label='targetAnglesFrontLeg', linewidth=1)
plt.xlabel("Steps")
plt.ylabel("Value in Radians")
plt.title("Motor Commands")
plt.legend()
plt.show()

# backLegSensorValues = np.load("data/backLegSensorData.npy")
# frontLegSensorValues = np.load("data/frontLegSensorData.npy")
# plt.plot(backLegSensorValues, label="Back Leg", linewidth=3)
# plt.plot(frontLegSensorValues, label="Front Leg", linewidth=0.5)
# plt.legend()
# plt.show()