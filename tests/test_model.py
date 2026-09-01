"""Pruebas automáticas para el modelo de formación de mercado."""

import numpy as np
import pytest

from src.model import (
    S0,
    execution_probability,
    informed_ask_loss,
    optimize_quotes,
)


def test_execution_probability_is_never_negative():
    """La probabilidad de ejecución nunca debe ser negativa."""
    spreads = np.array([0.0, 2.0, 6.25, 10.0, 100.0])
    probabilities = execution_probability(spreads)

    assert np.all(probabilities >= 0.0)


def test_informed_ask_loss_is_decreasing():
    """La pérdida informada debe disminuir cuando aumenta el Ask."""
    asks = [19.90, 20.50, 21.50]
    losses = [informed_ask_loss(ask) for ask in asks]

    assert losses[0] > losses[1] > losses[2]


def test_monopolist_solution_without_informed_traders():
    """
    Sin traders informados, el spread óptimo por lado debe ser 3.125.

La probabilidad llega a cero en 6.25, pero el máximo de
(0.50 - 0.08s)s se alcanza en 3.125.
    """
    result = optimize_quotes(pi_informed=0.0)

    ask_spread = result["ask"] - S0
    bid_spread = S0 - result["bid"]

    expected_spread_per_side = 0.50 / (2.0 * 0.08)      
    assert ask_spread == pytest.approx(expected_spread_per_side, abs=1e-3)
    assert bid_spread == pytest.approx(expected_spread_per_side, abs=1e-3)

