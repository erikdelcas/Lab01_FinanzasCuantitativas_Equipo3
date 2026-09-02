"""Ejecuta el laboratorio completo con el comando: python main.py."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.model import optimize_quotes, sensitivity_analysis
from src.plots import (
    plot_cumulative_inventory,
    plot_cumulative_pnl,
    plot_execution_probability,
    plot_monte_carlo_histogram,
    plot_sensitivity,
)
from src.simulation import run_monte_carlo, simulate_trades


SEED = 42
FIGURES_DIR = Path("docs/figures")


def main():
    """Ejecuta optimización, simulaciones, Monte Carlo y figuras."""
    np.random.seed(SEED)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("1. Calculando cotizaciones óptimas...")
    optimal = optimize_quotes()

    print(f"Bid óptimo: {optimal['bid']:.2f}")
    print(f"Ask óptimo: {optimal['ask']:.2f}")
    print(f"Spread óptimo: {optimal['spread']:.2f}")
    print(f"Utilidad esperada: {optimal['expected_profit']:.2f}")

    regimes = {
        "optimal": {
            "bid": optimal["bid"],
            "ask": optimal["ask"],
        },
        "tight": {
            "bid": 19.75,
            "ask": 20.05,
        },
        "wide": {
            "bid": 18.40,
            "ask": 21.40,
        },
    }

    print("\n2. Simulando 10,000 trades por régimen...")
    simulations = {}

    for index, (regime, quotes) in enumerate(regimes.items()):
        simulations[regime] = simulate_trades(
            bid=quotes["bid"],
            ask=quotes["ask"],
            n_trades=10_000,
            seed=SEED + index,
        )

        final_pnl = simulations[regime]["cumulative_pnl"].iloc[-1]
        final_inventory = simulations[regime][
            "cumulative_inventory"
        ].iloc[-1]

        print(
            f"{regime.capitalize()}: "
            f"P&L={final_pnl:.2f}, inventario={final_inventory}"
        )

    print("\n3. Ejecutando análisis Monte Carlo...")
    monte_carlo_results, monte_carlo_summary = run_monte_carlo(
        regimes=regimes,
        n_runs=1_000,
        trades_per_run=1_000,
        base_seed=1_000,
    )

    print(monte_carlo_summary.to_string(index=False))

    print("\n4. Ejecutando análisis de sensibilidad...")
    sensitivity_results = pd.DataFrame(sensitivity_analysis())

    print(
        sensitivity_results[
            ["pi_informed", "bid", "ask", "spread", "expected_profit"]
        ].round(4).to_string(index=False)
    )

    print("\n5. Generando figuras...")
    figures = {
        "01_execution_probability.png": plot_execution_probability(),
        "02_cumulative_pnl.png": plot_cumulative_pnl(simulations),
        "03_cumulative_inventory.png": plot_cumulative_inventory(simulations),
        "04_monte_carlo_histogram.png": plot_monte_carlo_histogram(
            monte_carlo_results
        ),
        "05_sensitivity.png": plot_sensitivity(sensitivity_results),
    }

    for filename, figure in figures.items():
        output_path = FIGURES_DIR / filename
        figure.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close(figure)

    print(f"Figuras guardadas en: {FIGURES_DIR}")
    print("\nProyecto ejecutado correctamente.")


if __name__ == "__main__":
    main()