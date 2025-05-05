import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import constants as c

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

plt.figure(figsize=(12, 7.5))
gs = plt.GridSpec(2, 1, height_ratios=[3, 1])

ax0 = plt.subplot(gs[0])

# for run in fitness_A:
#     ax0.plot(run, color='blue', alpha=0.1, linewidth=0.5)
# for run in fitness_B:
#     ax0.plot(run, color='red', alpha=0.1, linewidth=0.5)

ax0.plot(avg_fitness_A, label='Mean Fitness (A)', color='blue', linewidth=2)
ax0.fill_between(range(len(avg_fitness_A)), 
                 avg_fitness_A - std_fitness_A,
                 avg_fitness_A + std_fitness_A,
                 color='blue', alpha=0.2)

ax0.plot(avg_fitness_B, label='Mean Fitness (B)', color='red', linewidth=2)
ax0.fill_between(range(len(avg_fitness_B)), 
                 avg_fitness_B - std_fitness_B,
                 avg_fitness_B + std_fitness_B,
                 color='red', alpha=0.2)

sig_generations = np.where(p_values_smoothed < 0.05)[0]
for gen in sig_generations:
    if not np.isnan(p_values_smoothed[gen]):
        y_pos = max(avg_fitness_A[gen], avg_fitness_B[gen])
        ax0.plot(gen, y_pos, '*', color='black', markersize=10, zorder=5)

title_str = 'Evolution of Jumping Performance with Different Neural Architectures \n Test Variant A: 0 Hidden Neurons \n Test Variant B: 2 Hidden Neurons + Recurrent Connections'
ax0.set_title(title_str, pad=20)
ax0.set_ylabel('Fitness')
ax0.legend(loc='upper left')
ax0.grid(True, alpha=0.3)

ax1 = plt.subplot(gs[1])
ax1.plot(p_values_smoothed, color='black', label='p-value (smoothed)')
ax1.axhline(0.05, color='red', linestyle='--', label='Significance threshold (0.05)')
ax1.set_yscale('log')
ax1.set_xlabel('Generation')
ax1.set_ylabel('p-value (log scale)')
ax1.legend()
ax1.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig("data/fitness_comparison_with_stats.pdf", bbox_inches='tight')
plt.show()