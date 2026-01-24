# Entanglement Dominance Simulation

This repository contains the numerical verification code for the thesis:
**"Entanglement Dominance in the Zero-Temperature Limit"**
*Javier Manuel Martín Alonso (2026)*
https://doi.org/10.5281/zenodo.18361629

## Overview
This software reproduces **Theorem 4.3.1** and **Figure 4.1** of the manuscript. It maps the phase transition between thermal separability and topological entanglement in symmetric Two-Mode Squeezed Thermal (TMST) states.

## The Physics
The code solves the exact boundary where the symplectic eigenvalue $\tilde{\nu}_-$ drops below $1/2$. The "Entanglement Dominance" regime is defined where the squeezing parameter $r$ exceeds the thermal noise floor:

$$ r > \frac{1}{2} \ln(2\bar{n}(T) + 1) $$

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run simulation: `python main.py`

## Output
The script generates a phase diagram ![Phase Diagram](img/entanglement_phase_diagram.jpg) showing the critical temperature threshold for vacuum stability.

## License
MIT License



