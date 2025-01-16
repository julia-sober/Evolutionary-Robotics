import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x = 0
y = 0
z = 0.5

pyrosim.Start_SDF("boxes.sdf")

# loops for rows and columns of towers
for k in range(5):
    for j in range(5):
        # loop for tower height
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x+k,y+j,z+i] , size=[width*0.9**i,length*0.9**i,height*0.9**i])

pyrosim.End()