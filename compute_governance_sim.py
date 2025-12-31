import numpy as np
import matplotlib.pyplot as plt

# --- 1. Define the Physics of AI Training (Scaling Laws) ---
# This function MUST be defined before we use it below.
def calculate_loss(compute_flops, alpha=0.05, critical_compute=1e20):
    """
    Calculates the theoretical loss (error rate) of a model given a compute budget.
    Formula: L(C) = (Cc / C)^alpha
    """
    return (critical_compute / compute_flops) ** alpha

# --- 2. Simulation Parameters ---
# We simulate training runs from 10^18 FLOPS to 10^26 FLOPS
compute_budgets = np.logspace(18, 26, 100) 

# GOVERNMENT REGULATION: The "Cap"
# The US Government restricts training runs above 10^24 FLOPS
compute_cap = 1e24 

# --- 3. Monte Carlo Simulation (Modeling Uncertainty) ---
num_simulations = 1000
all_losses = []

# We assume alpha (scaling exponent) isn't exactly 0.05.
# We sample 1000 different possible worlds to show uncertainty.
np.random.seed(42)
alphas = np.random.normal(loc=0.05, scale=0.005, size=num_simulations)

# Run the simulation 1000 times
for alpha_sample in alphas:
    # This line works now because calculate_loss is defined above
    loss_run = calculate_loss(compute_budgets, alpha=alpha_sample)
    all_losses.append(loss_run)

all_losses = np.array(all_losses)

# Calculate Median and 90% Confidence Intervals
loss_unregulated_median = np.median(all_losses, axis=0)
lower_bound = np.percentile(all_losses, 5, axis=0)  # Best case
upper_bound = np.percentile(all_losses, 95, axis=0) # Worst case

# --- 4. Define Regulated Scenario (Based on Median) ---
loss_regulated = np.copy(loss_unregulated_median)
cap_index = np.searchsorted(compute_budgets, compute_cap)
loss_regulated[cap_index:] = loss_unregulated_median[cap_index] # Freeze at cap

# --- 5. Visualization ---
plt.figure(figsize=(10, 6))

# Plot the 90% Confidence Interval (The "Uncertainty Cloud")
plt.fill_between(compute_budgets, lower_bound, upper_bound, 
                 color='red', alpha=0.1, label='90% Confidence Interval (Scaling Uncertainty)')

# Plot Median Unregulated Growth
plt.plot(compute_budgets, loss_unregulated_median, 
         color='red', linestyle='--', linewidth=2, 
         label='Median Uncapped Training')

# Plot Regulated Growth
plt.plot(compute_budgets, loss_regulated, 
         color='green', linewidth=3, 
         label='Regulated Training (Compliance Cap)')

# Add the "Regulation Wall" line
plt.axvline(x=compute_cap, color='black', linestyle=':', label=f'Govt. Cap (10^24 FLOPS)')

# Formatting
plt.xscale('log')
plt.xlabel('Compute Budget (FLOPS)', fontsize=12)
plt.ylabel('Model Loss (Lower is Smarter)', fontsize=12)
plt.title('Impact of Hardware Caps on AI Model Capabilities\n(with Monte Carlo Uncertainty)', fontsize=14, fontweight='bold')
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.legend(loc='upper right')

# Annotation
plt.annotate('Capability Overhang', xy=(1e25, 0.78), xytext=(1e25, 0.82),
             arrowprops=dict(facecolor='black', shrink=0.05))

# Save and Show
plt.savefig("compute_governance_simulation_mc.png")
plt.show()

print("Simulation Complete. Monte Carlo Graph Generated.")