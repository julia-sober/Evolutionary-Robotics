from parallelHillClimber import PARALLEL_HILL_CLIMBER
import time
import constants as c
import os

os.system("rm log*.txt")
testVariant = "A"
phc = PARALLEL_HILL_CLIMBER(testVariant)
phc.Evolve()
phc.Show_Best()

time.sleep(c.numTimeSteps*c.sleepSize + 5)

os.system("rm log*.txt")
testVariant = "B"
phc = PARALLEL_HILL_CLIMBER(testVariant)
phc.Evolve()
phc.Show_Best()

time.sleep(c.numTimeSteps*c.sleepSize + 5)

os.system("rm log*.txt")
testVariant = "C"
phc = PARALLEL_HILL_CLIMBER(testVariant)
phc.Evolve()
phc.Show_Best()

time.sleep(c.numTimeSteps*c.sleepSize + 5)

os.system("python3 plotFitnessValues.py")
os.system("rm log*.txt")