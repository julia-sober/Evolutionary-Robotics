from parallelHillClimber import PARALLEL_HILL_CLIMBER
import time
import constants as c

testVariant = "A"
phc = PARALLEL_HILL_CLIMBER(testVariant)
phc.Evolve()
phc.Show_Best()

time.sleep(c.numTimeSteps*c.sleepSize + 5)

testVariant = "B"
phc = PARALLEL_HILL_CLIMBER(testVariant)
phc.Evolve()
phc.Show_Best()