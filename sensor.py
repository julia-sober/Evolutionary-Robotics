import numpy as np
import pyrosim.pyrosim as pyrosim

class SENSOR:
    
    def __init__(self, linkName, values):
        self.linkName = linkName
        self.values = values

    def Get_Value(self, timeStep):
        self.values[timeStep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        filename = "data/" + self.linkName + "SensorData.npy"
        np.save(filename, self.values)