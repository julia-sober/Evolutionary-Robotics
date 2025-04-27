import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import constants as c
import os

fitness_A = np.load("data/fitness_values_A.npy")
fitness_B = np.load("data/fitness_values_B.npy")

avg_fitness_A = np.nanmean(fitness_A, axis=0)
avg_fitness_B = np.nanmean(fitness_B, axis=0)
std_fitness_A = np.nanstd(fitness_A, axis=0)
std_fitness_B = np.nanstd(fitness_B, axis=0)

p_values = []
for gen in range(fitness_A.shape[1]):
    clean_A = fitness_A[:, gen][~np.isnan(fitness_A[:, gen])]
    clean_B = fitness_B[:, gen][~np.isnan(fitness_B[:, gen])]
    
    if len(clean_A) > 1 and len(clean_B) > 1:  
        _, p = stats.ttest_ind(clean_A, clean_B, equal_var=False)
        p_values.append(p)
    else:
        p_values.append(np.nan)

p_values = np.array(p_values)
p_values_smoothed = np.convolve(p_values, np.ones(3)/3, mode='same')  

plt.figure(figsize=(12, 10))
gs = plt.GridSpec(2, 1, height_ratios=[3, 1])

ax0 = plt.subplot(gs[0])

for run in fitness_A:
    ax0.plot(run, color='blue', alpha=0.1, linewidth=0.5)
for run in fitness_B:
    ax0.plot(run, color='red', alpha=0.1, linewidth=0.5)

# Plot averages with std deviation bands
ax0.plot(avg_fitness_A, label='Direct Connections (A)', color='navy', linewidth=2)
ax0.fill_between(range(len(avg_fitness_A)), 
                 avg_fitness_A - std_fitness_A,
                 avg_fitness_A + std_fitness_A,
                 color='blue', alpha=0.2)

ax0.plot(avg_fitness_B, label='Hidden+Recurrent (B)', color='darkred', linewidth=2)
ax0.fill_between(range(len(avg_fitness_B)), 
                 avg_fitness_B - std_fitness_B,
                 avg_fitness_B + std_fitness_B,
                 color='red', alpha=0.2)

# Mark statistically significant differences
sig_generations = np.where(p_values_smoothed < 0.05)[0]
for gen in sig_generations:
    if not np.isnan(p_values_smoothed[gen]):
        y_pos = max(avg_fitness_A[gen], avg_fitness_B[gen]) + 0.1
        ax0.plot(gen, y_pos, '*', color='black', markersize=10)

ax0.set_title('Evolution of Jumping Performance with Different Neural Architectures', pad=20)
ax0.set_ylabel('Fitness')
ax0.legend(loc='upper left')
ax0.grid(True, alpha=0.3)

# Bottom plot: Statistical significance
ax1 = plt.subplot(gs[1])
ax1.plot(p_values_smoothed, color='black', label='p-value (smoothed)')
ax1.axhline(0.05, color='red', linestyle='--', label='Significance threshold (0.05)')
ax1.set_yscale('log')
ax1.set_xlabel('Generation')
ax1.set_ylabel('p-value (log scale)')
ax1.legend()
ax1.grid(True, alpha=0.3)

plt.tight_layout()

# Save statistical results
with open("data/statistical_results.txt", "w") as f:
    f.write("Generation\tAvg_A\tStd_A\tAvg_B\tStd_B\tp-value\n")
    for gen in range(len(avg_fitness_A)):
        f.write(f"{gen}\t{avg_fitness_A[gen]:.3f}\t{std_fitness_A[gen]:.3f}\t"
                f"{avg_fitness_B[gen]:.3f}\t{std_fitness_B[gen]:.3f}\t{p_values[gen]:.4f}\n")

# Save plots
plt.savefig("data/fitness_comparison_with_stats.png", dpi=300, bbox_inches='tight')
plt.savefig("data/fitness_comparison_with_stats.pdf", bbox_inches='tight')
plt.show()

# Print final statistical comparison
final_gen = len(avg_fitness_A) - 1
print("\nFinal Generation Statistical Comparison:")
print(f"Variant A: Mean = {avg_fitness_A[final_gen]:.3f} ± {std_fitness_A[final_gen]:.3f}")
print(f"Variant B: Mean = {avg_fitness_B[final_gen]:.3f} ± {std_fitness_B[final_gen]:.3f}")
print(f"p-value = {p_values[final_gen]:.4f}")

if p_values[final_gen] < 0.05:
    print("Conclusion: Statistically significant difference at final generation (p < 0.05)")
else:
    print("Conclusion: No statistically significant difference at final generation (p ≥ 0.05)")


# import numpy as np
# import matplotlib.pyplot as plt
# import constants as c

# fitness_A = np.load("data/fitness_values_A.npy")
# fitness_B = np.load("data/fitness_values_B.npy")
# # fitness_C = np.load("data/fitness_values_C.npy")

# avg_fitness_A = np.nanmean(fitness_A, axis=0)
# avg_fitness_B = np.nanmean(fitness_B, axis=0)
# # avg_fitness_C = np.nanmean(fitness_C, axis=0)

# plt.figure(figsize=(10, 6))

# for ind, col in enumerate(fitness_A):
#     plt.plot(col, linewidth=0.6, color="blue", alpha=0.3)
# for ind, col in enumerate(fitness_B):
#     plt.plot(col, linewidth=0.6, color="red", alpha=0.3)
# # for ind, col in enumerate(fitness_C):
# #     plt.plot(col, linewidth=0.6, color="blue", alpha=0.3)

# plt.plot(avg_fitness_A, label="No Hidden Neurons or Recurrent Connections", linewidth=3, color="blue")
# plt.plot(avg_fitness_B, label="Hidden Neurons and Recurrent Connections", linewidth=3, color="red")
# # plt.plot(avg_fitness_C, label="Hidden Neurons but no Recurrent Connections", linewidth=3, color="blue")
# plt.title("Fitness Over Generations")
# plt.xlabel("Generation")
# plt.ylabel("Fitness")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()

# plt.show()

# plt.figure(figsize=(12, 7))  # Slightly larger figure

# # Individual runs with more descriptive alpha
# plt.plot(fitness_A.T, color="blue", alpha=0.15, linewidth=0.8)  # Transpose for cleaner plotting
# plt.plot(fitness_B.T, color="red", alpha=0.15, linewidth=0.8)

# # Averages with clearer styling
# plt.plot(avg_fitness_A, label="Direct Connections (A)", 
#          linewidth=3, color="navy", linestyle='-', marker='o', markersize=5, markevery=5)
# plt.plot(avg_fitness_B, label="Hidden+Recurrent (B)", 
#          linewidth=3, color="darkred", linestyle='-', marker='s', markersize=5, markevery=5)

# plt.title("Evolution of Jumping Performance\nComparison of Neural Architectures", pad=20)
# plt.xlabel("Generation", labelpad=10)
# plt.ylabel("Fitness (Jump Height × Duration)", labelpad=10)
# plt.legend(framealpha=1, loc='upper left')  # More visible legend
# plt.grid(True, alpha=0.3)

# # Add some annotations
# max_A, max_B = np.nanmax(avg_fitness_A), np.nanmax(avg_fitness_B)
# plt.annotate(f'Max: {max_A:.2f}', xy=(len(avg_fitness_A)-1, avg_fitness_A[-1]), 
#              xytext=(10,10), textcoords='offset points', color='navy')
# plt.annotate(f'Max: {max_B:.2f}', xy=(len(avg_fitness_B)-1, avg_fitness_B[-1]), 
#              xytext=(10,-15), textcoords='offset points', color='darkred')

# plt.tight_layout()
# plt.savefig("fitness_comparison.png", dpi=300)  # Save high-quality version
# plt.show()
