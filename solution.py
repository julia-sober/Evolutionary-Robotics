import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:

    def __init__(self, myID, testVariant):
        self.myID = myID
        self.testVariant = testVariant

        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1

        self.sensorToHiddenWeights = np.random.rand(c.numSensorNeurons, c.numHiddenNeurons)
        self.sensorToHiddenWeights = self.sensorToHiddenWeights * 2 - 1

        self.hiddenToMotorWeights = np.random.rand(c.numHiddenNeurons, c.numMotorNeurons)
        self.hiddenToMotorWeights = self.hiddenToMotorWeights * 2 - 1

        self.recurrentWeights = np.random.rand(c.numHiddenNeurons, c.numHiddenNeurons)
        self.recurrentWeights = self.recurrentWeights * 2 - 1
        
    def Start_Simulation(self, directOrGUI):
        # self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        # os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1" + " &")
        # os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &")
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} >log{self.myID}.txt 2>&1 &")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        ctr = 0
        while not os.path.exists(fitnessFileName):      
            time.sleep(0.01)
            ctr += 1
            if ctr % 200 == 0:
                print()
                print()
                print("Looking for:", os.path.abspath(fitnessFileName))
                print("Current dir:", os.getcwd())
                print(f"Waiting for {fitnessFileName}... ({ctr*10}ms)")
            if ctr >= 1000:
                print()
                print()
                print("Quitting...")
                print("Error with " + fitnessFileName)
                exit()
        ctr = 0
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.readline())
        fitnessFile.close()
        os.system("rm " + fitnessFileName)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1], size=[1,1,1])

        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child ="BackLeg", type="revolute", position=[0,-0.5,1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0], size=[0.2,1,0.2])

        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0,0.5,1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0], size=[0.2,1,0.2])

        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5,0,1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0], size=[1,0.2,0.2])

        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0.5,0,1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0], size=[1,0.2,0.2])

        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])

        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0,-1,0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])

        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1,0,0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])

        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1,0,0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])

        pyrosim.End()

    def Create_Brain(self):
        if self.testVariant == "A":
            pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
    
            pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLowerLeg")

            pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_BackLeg")
            pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FrontLeg")
            pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
            pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
            pyrosim.Send_Motor_Neuron(name=8, jointName="FrontLeg_FrontLowerLeg")
            pyrosim.Send_Motor_Neuron(name=9, jointName="BackLeg_BackLowerLeg")
            pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LeftLowerLeg")
            pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_RightLowerLeg")

            for currentRow in range(0,c.numSensorNeurons):
                for currentColumn in range(0,c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons, 
                                        weight=self.weights[currentRow][currentColumn])
                
            pyrosim.End()

        elif self.testVariant == "B":
            pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
  
            pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLowerLeg")

            pyrosim.Send_Hidden_Neuron(name=4)
            pyrosim.Send_Hidden_Neuron(name=5)
            pyrosim.Send_Hidden_Neuron(name=6)
            pyrosim.Send_Hidden_Neuron(name=7)
            pyrosim.Send_Hidden_Neuron(name=8)
            pyrosim.Send_Hidden_Neuron(name=9)
            pyrosim.Send_Hidden_Neuron(name=10)
            pyrosim.Send_Hidden_Neuron(name=11)
            pyrosim.Send_Hidden_Neuron(name=12)
            pyrosim.Send_Hidden_Neuron(name=13)
            pyrosim.Send_Hidden_Neuron(name=14)
            pyrosim.Send_Hidden_Neuron(name=15)
            pyrosim.Send_Hidden_Neuron(name=16)
            pyrosim.Send_Hidden_Neuron(name=17)
            pyrosim.Send_Hidden_Neuron(name=18)
            pyrosim.Send_Hidden_Neuron(name=19)

            pyrosim.Send_Motor_Neuron(name=20, jointName="Torso_BackLeg")
            pyrosim.Send_Motor_Neuron(name=21, jointName="Torso_FrontLeg")
            pyrosim.Send_Motor_Neuron(name=22, jointName="Torso_LeftLeg")
            pyrosim.Send_Motor_Neuron(name=23, jointName="Torso_RightLeg")
            pyrosim.Send_Motor_Neuron(name=24, jointName="FrontLeg_FrontLowerLeg")
            pyrosim.Send_Motor_Neuron(name=25, jointName="BackLeg_BackLowerLeg")
            pyrosim.Send_Motor_Neuron(name=26, jointName="LeftLeg_LeftLowerLeg")
            pyrosim.Send_Motor_Neuron(name=27, jointName="RightLeg_RightLowerLeg")

            for currentRow in range(0,c.numSensorNeurons):
                for currentColumn in range(0,c.numHiddenNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons, 
                                        weight=self.sensorToHiddenWeights[currentRow][currentColumn])
                    
            for currentRow in range(0,c.numHiddenNeurons):
                for currentColumn in range(0,c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow+c.numSensorNeurons, 
                                        targetNeuronName=currentColumn+c.numHiddenNeurons+c.numSensorNeurons, 
                                        weight=self.hiddenToMotorWeights[currentRow][currentColumn])
                    
            for currentRow in range(0,c.numHiddenNeurons):
                for currentColumn in range(0,c.numHiddenNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow+c.numSensorNeurons, targetNeuronName=currentColumn+c.numSensorNeurons, 
                                        weight=self.recurrentWeights[currentRow][currentColumn])
                
            pyrosim.End()

        elif self.testVariant == "C":
            pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
  
            pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLowerLeg")
            pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLowerLeg")

            pyrosim.Send_Hidden_Neuron(name=4)
            pyrosim.Send_Hidden_Neuron(name=5)
            pyrosim.Send_Hidden_Neuron(name=6)
            pyrosim.Send_Hidden_Neuron(name=7)
            pyrosim.Send_Hidden_Neuron(name=8)
            pyrosim.Send_Hidden_Neuron(name=9)
            pyrosim.Send_Hidden_Neuron(name=10)
            pyrosim.Send_Hidden_Neuron(name=11)
            pyrosim.Send_Hidden_Neuron(name=12)
            pyrosim.Send_Hidden_Neuron(name=13)
            pyrosim.Send_Hidden_Neuron(name=14)
            pyrosim.Send_Hidden_Neuron(name=15)
            pyrosim.Send_Hidden_Neuron(name=16)
            pyrosim.Send_Hidden_Neuron(name=17)
            pyrosim.Send_Hidden_Neuron(name=18)
            pyrosim.Send_Hidden_Neuron(name=19)

            pyrosim.Send_Motor_Neuron(name=20, jointName="Torso_BackLeg")
            pyrosim.Send_Motor_Neuron(name=21, jointName="Torso_FrontLeg")
            pyrosim.Send_Motor_Neuron(name=22, jointName="Torso_LeftLeg")
            pyrosim.Send_Motor_Neuron(name=23, jointName="Torso_RightLeg")
            pyrosim.Send_Motor_Neuron(name=24, jointName="FrontLeg_FrontLowerLeg")
            pyrosim.Send_Motor_Neuron(name=25, jointName="BackLeg_BackLowerLeg")
            pyrosim.Send_Motor_Neuron(name=26, jointName="LeftLeg_LeftLowerLeg")
            pyrosim.Send_Motor_Neuron(name=27, jointName="RightLeg_RightLowerLeg")

            for currentRow in range(0,c.numSensorNeurons):
                for currentColumn in range(0,c.numHiddenNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons, 
                                        weight=self.sensorToHiddenWeights[currentRow][currentColumn])
                    
            for currentRow in range(0,c.numHiddenNeurons):
                for currentColumn in range(0,c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow+c.numSensorNeurons, 
                                        targetNeuronName=currentColumn+c.numHiddenNeurons+c.numSensorNeurons, 
                                        weight=self.hiddenToMotorWeights[currentRow][currentColumn])
                
            pyrosim.End()

    def Mutate(self):
        if self.testVariant == "A":
            for _ in range(c.mutationRate):
                randomRow = random.randint(0,c.numSensorNeurons-1)
                randomColumn = random.randint(0,c.numMotorNeurons-1)
                self.weights[randomRow][randomColumn] = random.random() * 2 - 1

        if self.testVariant == "B":
            for _ in range(c.mutationRate):
                randomRow = random.randint(0,c.numSensorNeurons-1)
                randomColumn = random.randint(0,c.numHiddenNeurons-1)
                self.sensorToHiddenWeights[randomRow][randomColumn] = random.random() * 2 - 1
                randomRow = random.randint(0,c.numHiddenNeurons-1)
                randomColumn = random.randint(0,c.numMotorNeurons-1)
                self.hiddenToMotorWeights[randomRow][randomColumn] = random.random() * 2 - 1
                randomRow = random.randint(0,c.numHiddenNeurons-1)
                randomColumn = random.randint(0,c.numHiddenNeurons-1)
                self.recurrentWeights[randomRow][randomColumn] = random.random() * 2 - 1

        elif self.testVariant == "C":
            for _ in range(c.mutationRate):
                randomRow = random.randint(0,c.numSensorNeurons-1)
                randomColumn = random.randint(0,c.numHiddenNeurons-1)
                self.sensorToHiddenWeights[randomRow][randomColumn] = random.random() * 2 - 1
                randomRow = random.randint(0,c.numHiddenNeurons-1)
                randomColumn = random.randint(0,c.numMotorNeurons-1)
                self.hiddenToMotorWeights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, newID):
        self.myID = newID