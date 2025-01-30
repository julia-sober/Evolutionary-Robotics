import pybullet as p
import pybullet_data
import time

physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.setGravity(0, 0, -9.8)
p.loadSDF("world.sdf")

for i in range(1000):
    p.stepSimulation()
    time.sleep(1/60)
    print(f"Iteration {i+1}")

p.disconnect()