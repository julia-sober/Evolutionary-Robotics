import numpy as np
import matplotlib.pyplot as plt
import constants as c

fitness_A = np.load("data/fitness_values_A.npy")
fitness_B = np.load("data/fitness_values_B.npy")
fitness_C = np.load("data/fitness_values_C.npy")

avg_fitness_A = np.mean(fitness_A, axis=0)
avg_fitness_B = np.mean(fitness_B, axis=0)
avg_fitness_C = np.mean(fitness_C, axis=0)

plt.figure(figsize=(10, 6))
plt.plot(avg_fitness_A, label="No Hidden Neurons", linewidth=2, color="blue")
plt.plot(avg_fitness_B, label="Hidden Neurons + Recurrent Connections", linewidth=2, color="orange")
plt.plot(avg_fitness_C, label="Hidden Neurons, No Recurrent Connections", linewidth=2, color="red")
plt.title("Average Fitness Over Generations")
plt.xlabel("Generation")
plt.ylabel("Average Fitness")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
