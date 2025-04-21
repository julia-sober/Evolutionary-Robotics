import pybullet as p

class WORLD:
    
    def __init__(self):
        try:
            p.loadSDF("world.sdf")
        except Exception as e:
            print(f"Failed to load world: {e}")
            raise e  
        self.planeId = p.loadURDF("plane.urdf")