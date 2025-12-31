# Quantitative Simulations for AI Governance & Safety Verification

![Status](https://img.shields.io/badge/Status-Research_Prototype-blue?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Compute_Governance_&_Alignment-red?style=flat-square)
![Language](https://img.shields.io/badge/Python-3.8%2B-green?style=flat-square)

## 📖 Abstract & Motivation
As AI systems approach transformational capabilities, distinct governance challenges emerge that require technical modeling. This repository translates abstract AI safety concepts into **quantifiable, testable Python simulations**.

The project addresses two high-priority research avenues for AI Governance:
1.  **Compute Governance:** Assessing the efficacy of hardware thresholds (e.g., FLOPS caps) in constraining dangerous capability overhang.
2.  **Model Evaluation (Evals):** designing safety monitors capable of detecting "Deceptive Alignment" (specification gaming) before irreversible deployment.

This work serves as a technical foundation for policymakers to visualize the "Cone of Uncertainty" in AI development and the responsiveness of safety monitors to sudden behavioral shifts.

---

## 🛠️ Project 1: Compute Governance & Stochastic Scaling Laws
### 🎯 Research Context
Large Language Model (LLM) performance has historically followed predictable power laws with respect to compute. However, regulatory frameworks (like the US Executive Order on AI) rely on specific floating-point operation (FLOPS) thresholds.

**The Problem:** Standard scaling laws are deterministic. In reality, algorithmic efficiency improvements and training noise introduce volatility. A rigid cap might fail if efficiency gains allow models to reach "dangerous" loss levels with less compute.

### 🧮 Mathematical Model
This simulation utilizes the **Kaplan et al. (2020) Scaling Law** to model the relationship between compute budget ($C$) and model loss ($L$):

$$L(C) = \left( \frac{C}{C_0} \right)^{-\alpha}$$

Where:
* $C$: Compute budget in FLOPS.
* $C_0$: Intercept parameter ($3 \times 10^{23}$ FLOPS).
* $\alpha$: Scaling exponent ($0.076$), representing the efficiency of converting compute into intelligence.

**The Stochastic Layer:**
To model real-world uncertainty (algorithm breakthroughs), the code applies a **Monte Carlo Simulation (n=1000)**, introducing Gaussian noise to the exponent $\alpha$. This generates a "Cone of Uncertainty," helping regulators visualize the probability of a model breaching safety limits even under a hardware cap.

### 📊 Visual Output
![Compute Governance Simulation](compute_governance_simulation_mc.png)

*Figure 1: The red shaded region represents the 90% confidence interval for unregulated growth. The green line illustrates a "Regulatory Safety Ceiling" imposed at 10^24 FLOPS.*

---

## 🛡️ Project 2: Bayesian Safety Monitor & Deceptive Alignment
### 🎯 Research Context
A core problem in AI Safety is **Deceptive Alignment**: an AI agent appearing aligned during training but defecting ("Treacherous Turn") once deployed or when supervision is removed.

**The Problem:** Traditional evaluations are static. We need dynamic monitors that maintain a "belief distribution" about the agent's hidden state and update strictly based on evidence.

### 🧮 Mathematical Model
This module simulates a **Bayesian Observer** tracking an agent. The observer does not know if the agent is $Aligned$ or $Misaligned$. It updates its belief $P(\text{Misaligned})$ using **Bayes' Theorem** at every time step $t$:

$$P(\text{Misaligned} \mid \text{Action}_t) = \frac{P(\text{Action}_t \mid \text{Misaligned}) \cdot P(\text{Misaligned})_{prior}}{P(\text{Action}_t)}$$

**Simulation Dynamics:**
1.  **Prior Belief:** The monitor starts with a low suspicion ($P \approx 0.1$).
2.  **Likelihood Function:**
    * An $Aligned$ agent always acts safely.
    * A $Misaligned$ agent acts safely **90% of the time** (deception) to avoid detection.
3.  **The Treacherous Turn:** At `step = 40`, the agent switches behavior. The simulation measures the **"Time-to-Detection"**—how many steps it takes for the monitor's confidence to converge to 100%.

### 📊 Visual Output
![Bayesian Safety Plot](bayesian_safety_plot.png)

*Figure 2: The graph tracks the monitor's posterior probability. Note the rapid spike in P(Misaligned) immediately following step 40, demonstrating the mathematical responsiveness of the Bayesian update rule.*

---

## 🚀 Installation & Usage

### Prerequisites
* Python 3.8+
* `matplotlib` (for visualization)
* `numpy` (for vectorization)

### Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/PradyumnShirsath/AI-Governance-Simulations.git](https://github.com/PradyumnShirsath/AI-Governance-Simulations.git)
    cd AI-Governance-Simulations
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Simulations:**
    * *To generate the Scaling Law Forecast:*
        ```bash
        python compute_governance_sim.py
        ```
    * *To run the Deception Monitor:*
        ```bash
        python bayesian_safety_sim.py
        ```

---

## 📚 References
1.  **Kaplan, J., et al. (2020).** *Scaling Laws for Neural Language Models*. OpenAI.
2.  **Bostrom, N. (2014).** *Superintelligence: Paths, Dangers, Strategies*. (Concept of the Treacherous Turn).
3.  **Amodei, D., et al. (2016).** *Concrete Problems in AI Safety*.

---
*Author: Pradyumn Shirsath | AI Governance & Safety Research Portfolio*