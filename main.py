"""
Entanglement Dominance in the Zero-Temperature Limit
Simulation & Visualization of Theorem 4.3.1 (Symmetric TMST Threshold)

Reference:
Martín Alonso, J. M. (2026). "Entanglement Dominance in the Zero-Temperature Limit".
Zenodo. https://doi.org/10.5281/zenodo.18353640

Description:
This script calculates the exact entanglement threshold for a Two-Mode Squeezed 
Thermal State (TMST) undergoing Markovian thermalization. It generates a Phase Diagram 
mapping the 'Entanglement-Dominant Regime' vs. 'Thermal-Noise Dominated Regime'.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ==========================================
# USER CONFIGURATION (Change these to test limits)
# ==========================================
OMEGA = 1.0           # Mode frequency (Natural units)
TEMP_MIN = 0.01       # Minimum Temperature (avoid exactly 0 for log stability)
TEMP_MAX = 3.0        # Maximum Temperature (k_B T / hbar omega)
SQUEEZING_MAX = 2.0   # Maximum Squeezing Parameter (r)
GRID_RESOLUTION = 500 # Points per axis (higher = smoother, slower)
OUTPUT_FILENAME = "entanglement_phase_diagram.png"
SHOW_PLOT = True      # Set to False to run in headless environments
# ==========================================

def bose_einstein(temp, omega=OMEGA):
    """Calculates mean thermal occupation number n_bar."""
    # Avoid division by zero at T=0
    with np.errstate(divide='ignore', invalid='ignore'):
        n = 1.0 / (np.exp(omega / temp) - 1.0)
    # Correcting for T near zero where exp goes to infinity
    n = np.nan_to_num(n, nan=0.0) 
    return n

def critical_squeezing(n_bar):
    """
    Analytic Threshold (Theorem 4.3.1):
    r_c(T) = 0.5 * ln(2*n_bar + 1)
    """
    return 0.5 * np.log(2 * n_bar + 1)

def log_negativity(r, n_bar):
    """
    Calculates Logarithmic Negativity E_N.
    E_N = max(0, -log2(2 * nu_minus))
    where nu_minus = (n_bar + 0.5) * exp(-2r)
    """
    nu_minus = (n_bar + 0.5) * np.exp(-2 * r)
    val = -np.log2(2 * nu_minus)
    return np.maximum(0, val)

def run_simulation():
    print(f"Starting simulation with T_max={TEMP_MAX}, r_max={SQUEEZING_MAX}...")
    
    # --- SIMULATION GRID ---
    T_vals = np.linspace(TEMP_MIN, 5.0, GRID_RESOLUTION) # Extended slightly for visuals
    r_vals = np.linspace(0, SQUEEZING_MAX, GRID_RESOLUTION)

    T_grid, r_grid = np.meshgrid(T_vals, r_vals)
    n_bar_grid = bose_einstein(T_grid)

    # --- CALCULATE ENTANGLEMENT LANDSCAPE ---
    E_N = log_negativity(r_grid, n_bar_grid)

    # --- CALCULATE EXACT ANALYTIC THRESHOLD ---
    # We calculate r_critical for the T_vals array to draw the line
    n_bar_line = bose_einstein(T_vals)
    r_crit_line = critical_squeezing(n_bar_line)

    # --- PLOTTING ---
    plt.figure(figsize=(10, 7))

    # Custom Colormap: White (Separable) -> Blue/Purple (Entangled)
    colors = ["#f0f0f0", "#d1e5f0", "#4393c3", "#2166ac", "#053061"]
    cmap = LinearSegmentedColormap.from_list("entanglement_map", colors, N=100)

    # 1. Plot Heatmap of Entanglement Strength
    contour = plt.contourf(T_grid, r_grid, E_N, levels=50, cmap=cmap)
    cbar = plt.colorbar(contour)
    cbar.set_label(r'Log-Negativity $E_N$ (Entanglement Bits)', fontsize=12)

    # 2. Plot the Exact Analytic Threshold Line
    plt.plot(T_vals, r_crit_line, 'r-', linewidth=2.5, label=r'Analytic Threshold $r_c(T)$')

    # 3. Annotations
    plt.fill_between(T_vals, 0, r_crit_line, color='gray', alpha=0.1, hatch='///')
    plt.text(TEMP_MAX/3, 0.2, 'NOISE DOMINATED\n(Separable)', fontsize=14, color='#555555', ha='center', fontweight='bold')
    plt.text(TEMP_MAX/2, SQUEEZING_MAX*0.75, 'ENTANGLEMENT DOMINANT\n(Topological Channel Open)', fontsize=14, color='white', ha='center', fontweight='bold')

    # Formatting
    plt.title(f'Phase Diagram: Entanglement Dominance in TMST\n(Verification of Thesis Theorem 4.3.1)', fontsize=14)
    plt.xlabel(r'Temperature ($k_B T / \hbar \omega$)', fontsize=12)
    plt.ylabel(r'Squeezing Parameter $r$', fontsize=12)
    plt.ylim(0, SQUEEZING_MAX)
    plt.xlim(0, TEMP_MAX)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='upper right', framealpha=1.0)

    # Save output
    plt.savefig(OUTPUT_FILENAME, dpi=300)
    print(f"Simulation complete. '{OUTPUT_FILENAME}' generated.")
    
    if SHOW_PLOT:
        plt.show()

if __name__ == "__main__":
    run_simulation()

