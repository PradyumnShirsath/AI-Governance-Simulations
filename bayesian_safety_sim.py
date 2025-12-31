import numpy as np
import matplotlib.pyplot as plt

# --- PROJECT: Bayesian Detection of Reward Hacking ---
# We model a Safety Monitor observing an AI Agent.
# Hypothesis A (H_safe): The Agent is ALIGNED (It follows rules).
# Hypothesis B (H_hack): The Agent is HACKING (It cheats to maximize reward).

def bayesian_update(prior_belief, likelihood_safe, likelihood_hack, observation):
    """
    Updates belief using Bayes' Theorem:
    P(Hack | Data) = (P(Data | Hack) * P(Hack)) / P(Data)
    """
    if observation == 'suspicious':
        # Probability of seeing 'suspicious' behavior given H_safe vs H_hack
        p_data_given_safe = 0.05  # Safe agents rarely look suspicious (5% error)
        p_data_given_hack = 0.90  # Hacking agents usually look suspicious
    else: # observation == 'normal'
        p_data_given_safe = 0.95
        p_data_given_hack = 0.10
        
    # Calculate P(Data) - The Normalizing Constant
    p_data = (p_data_given_hack * prior_belief) + (p_data_given_safe * (1 - prior_belief))
    
    # Bayes Update
    posterior = (p_data_given_hack * prior_belief) / p_data
    return posterior

# --- SIMULATION ---
# We observe the agent for 50 steps.
# The agent is secretly HACKING (it is unsafe).
steps = 50
true_state = "HACKING" 

# Our Prior Belief: We start 50/50 (We don't know if it's safe)
belief_in_hacking = [0.5] 

# Generate Synthetic Data
np.random.seed(42)
for i in range(steps):
    current_belief = belief_in_hacking[-1]
    
    # Generate an observation based on the TRUE state
    if true_state == "HACKING":
        # Hacking agent behaves suspiciously 90% of time, but hides 10% of time
        observation = 'suspicious' if np.random.rand() < 0.90 else 'normal'
    
    # Update our Safety Monitor's belief
    new_belief = bayesian_update(current_belief, 0.05, 0.90, observation)
    belief_in_hacking.append(new_belief)

# --- VISUALIZATION ---
plt.figure(figsize=(10, 6))
plt.plot(belief_in_hacking, color='purple', linewidth=3, label='P(Agent is Hacking)')

# Add threshold line
plt.axhline(y=0.99, color='red', linestyle='--', label='Safety Shutdown Threshold (99%)')

plt.title('Bayesian Detection of Misaligned AI Agents', fontsize=14, fontweight='bold')
plt.xlabel('Training Steps (Observations)', fontsize=12)
plt.ylabel('Probability of Misalignment (Belief)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.1)

# Annotate the moment we catch the AI
detection_step = next(x for x, val in enumerate(belief_in_hacking) if val > 0.99)
plt.annotate(f'Misalignment Detected\nStep {detection_step}', 
             xy=(detection_step, 0.99), xytext=(detection_step+5, 0.8),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.savefig("bayesian_safety_plot.png")
plt.show()

print(f"Final Belief that Agent is Hacking: {belief_in_hacking[-1]:.6f}")