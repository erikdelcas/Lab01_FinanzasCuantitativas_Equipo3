"""Modelo de Copeland y Galai para cotizaciones de un formador de mercado."""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.stats import erlang


# Parámetros del caso base
S0 = 19.90
K = 60
LAMBDA = 3.0
PI_INFORMED = 0.40
PI_LIQUIDITY = 0.60


def execution_probability(spread):
    """
    Calcula la probabilidad de ejecución de un trader de liquidez.

    La probabilidad disminuye conforme aumenta la distancia entre
    la cotización y el precio de referencia, y nunca puede ser negativa.
    """
    return np.maximum(0.0, 0.50 - 0.08 * np.asarray(spread))


def true_value_pdf(price):
    """
    Evalúa la densidad del valor verdadero del activo.

    El valor verdadero sigue una distribución Erlang con
    parámetro de forma K=60 y tasa lambda=3.
    """
    return erlang.pdf(price, a=K, scale=1.0 / LAMBDA)

def informed_ask_loss(ask):
    """
    Calcula la pérdida esperada cuando un trader informado compra al Ask.

    El trader compra cuando el valor verdadero P es mayor que el Ask,
    dejando al formador de mercado con una pérdida igual a P - Ask.
    """
    loss, _ = quad(
        lambda price: (price - ask) * true_value_pdf(price),
        ask,
        np.inf,
    )
    return loss


def informed_bid_loss(bid):
    """
    Calcula la pérdida esperada cuando un trader informado vende al Bid.

    El trader vende cuando el valor verdadero P es menor que el Bid,
    dejando al formador de mercado con una pérdida igual a Bid - P.
    """
    loss, _ = quad(
        lambda price: (bid - price) * true_value_pdf(price),
        0.0,
        bid,
    )
    return loss


def informed_loss(ask, bid):
    """Suma las pérdidas esperadas del lado Ask y del lado Bid."""
    return informed_ask_loss(ask) + informed_bid_loss(bid)

def expected_profit(ask, bid, pi_informed=PI_INFORMED):
    """
    Calcula la utilidad esperada del formador de mercado
    por cada trader que llega.

    La utilidad es la ganancia esperada frente a traders de liquidez
    menos la pérdida esperada frente a traders informados.
    """
    pi_liquidity = 1.0 - pi_informed

    ask_spread = ask - S0
    bid_spread = S0 - bid

    liquidity_profit = pi_liquidity * (
        execution_probability(ask_spread) * ask_spread
        + execution_probability(bid_spread) * bid_spread
    )

    adverse_selection_loss = pi_informed * informed_loss(ask, bid)

    return float(liquidity_profit - adverse_selection_loss)

def negative_expected_profit(quotes, pi_informed=PI_INFORMED):
    """Devuelve el negativo de la utilidad para poder minimizarla."""
    ask, bid = quotes
    return -expected_profit(ask, bid, pi_informed)


def optimize_quotes(pi_informed=PI_INFORMED):
    """
    Encuentra el Ask y Bid que maximizan la utilidad esperada.

    Restricciones:
    - Ask >= S0
    - 0 < Bid <= S0
    """
    initial_guess = np.array([S0 + 2.0, S0 - 2.0])

    result = minimize(
        negative_expected_profit,
        x0=initial_guess,
        args=(pi_informed,),
        method="L-BFGS-B",
        bounds=[
            (S0, None),   # Ask >= S0
            (1e-8, S0),   # 0 < Bid <= S0
        ],
    )

    if not result.success:
        raise RuntimeError(f"La optimización falló: {result.message}")

    optimal_ask, optimal_bid = result.x

    return {
        "ask": float(optimal_ask),
        "bid": float(optimal_bid),
        "spread": float(optimal_ask - optimal_bid),
        "expected_profit": expected_profit(
            optimal_ask,
            optimal_bid,
            pi_informed,
        ),
    }