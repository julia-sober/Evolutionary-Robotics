import os
from hillclimber import HILLCLIMBER
from solution import SOLUTION

hc = HILLCLIMBER()
solution = SOLUTION()
hc.Evolve()

# for i in range(5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")