"""Funciones para generar las figuras obligatorias del laboratorio."""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.model import execution_probability


sns.set_theme(style="whitegrid")


def plot_execution_probability():
    """Grafica la probabilidad de ejecución contra el spread por lado."""
    spreads = np.linspace(0.0, 8.0, 200)
    probabilities = execution_probability(spreads)
    zero_point = 0.50 / 0.08

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        spreads,
        probabilities,
        color="navy",
        linewidth=2,
        label="Probabilidad de ejecución",
    )
    ax.axvline(
        zero_point,
        color="red",
        linestyle="--",
        label=f"Probabilidad cero: s = {zero_point:.2f}",
    )
    ax.scatter(zero_point, 0.0, color="red", zorder=3)

    ax.set_title("Probabilidad de ejecución contra spread")
    ax.set_xlabel("Spread por lado")
    ax.set_ylabel("Probabilidad de ejecución")
    ax.legend()

    fig.tight_layout()
    return fig


def plot_cumulative_pnl(simulations):
    """Compara el P&L acumulado de los tres regímenes."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for regime, trades in simulations.items():
        ax.plot(
            trades["trade"],
            trades["cumulative_pnl"],
            label=regime.capitalize(),
        )

    ax.set_title("P&L acumulado durante 10,000 trades")
    ax.set_xlabel("Número de trade")
    ax.set_ylabel("P&L acumulado")
    ax.legend()

    fig.tight_layout()
    return fig


def plot_cumulative_inventory(simulations):
    """Compara el inventario acumulado de los tres regímenes."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for regime, trades in simulations.items():
        ax.plot(
            trades["trade"],
            trades["cumulative_inventory"],
            label=regime.capitalize(),
        )

    ax.set_title("Inventario acumulado durante 10,000 trades")
    ax.set_xlabel("Número de trade")
    ax.set_ylabel("Inventario acumulado")
    ax.legend()

    fig.tight_layout()
    return fig


def plot_monte_carlo_histogram(monte_carlo_results):
    """Grafica la distribución del P&L final de Monte Carlo."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for regime in monte_carlo_results["regime"].unique():
        values = monte_carlo_results.loc[
            monte_carlo_results["regime"] == regime,
            "final_pnl",
        ]

        ax.hist(
            values,
            bins=30,
            alpha=0.50,
            label=regime.capitalize(),
        )

    ax.axvline(0.0, color="black", linestyle="--", label="P&L = 0")
    ax.set_title("Distribución del P&L final: Monte Carlo")
    ax.set_xlabel("P&L final")
    ax.set_ylabel("Frecuencia")
    ax.legend()

    fig.tight_layout()
    return fig


def plot_sensitivity(sensitivity_results):
    """Grafica el spread óptimo contra la proporción informada."""
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        sensitivity_results["pi_informed"],
        sensitivity_results["spread"],
        marker="o",
        linewidth=2,
        color="darkgreen",
        label="Spread óptimo",
    )

    ax.set_title("Spread óptimo contra proporción de traders informados")
    ax.set_xlabel("Probabilidad de trader informado")
    ax.set_ylabel("Spread óptimo")
    ax.set_xticks(sensitivity_results["pi_informed"])
    ax.legend()

    fig.tight_layout()
    return fig