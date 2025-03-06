import pyrosim.pyrosim as pyrosim
import random

length = 1
width = 1
height = 1

x = 0
y = 0
z = 0.5

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-2,2,0.5] , size=[width,length,height])
    pyrosim.End()

def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5], size=[width,length,height])
    pyrosim.Send_Joint(name ="Torso_BackLeg", parent= "Torso", child = "BackLeg", type = "revolute", position = [1,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5], size=[width,length,height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5], size=[width,length,height])
    pyrosim.End()

def Generate_Brain():
    sensorNeurons = []
    motorNeurons = []

    pyrosim.Start_NeuralNetwork("brain.nndf")

    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    sensorNeurons.append(0)
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    sensorNeurons.append(1)
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
    sensorNeurons.append(2)

    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    motorNeurons.append(3)
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
    motorNeurons.append(4)

    for i in sensorNeurons:
        for j in motorNeurons:
            pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=j, weight=random.randrange(-1,1))

    pyrosim.End()

Create_World()
Generate_Body()
Generate_Brain()