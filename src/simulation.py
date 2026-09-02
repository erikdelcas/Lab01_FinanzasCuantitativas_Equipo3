"""Simulación de operaciones para distintos regímenes de cotización."""

import numpy as np
import pandas as pd

from src.model import (
    K,
    LAMBDA,
    PI_INFORMED,
    S0,
    execution_probability,
)


def simulate_trades(
    bid,
    ask,
    n_trades=10_000,
    pi_informed=PI_INFORMED,
    seed=42,
):
    """
    Simula operaciones ejecutadas contra el formador de mercado.

    Si el trader es informado, opera solamente cuando el valor verdadero
    está fuera del Bid-Ask. Si es de liquidez, su operación se ejecuta
    conforme a la función de probabilidad de ejecución.
    """
    np.random.seed(seed)

    records = []

    while len(records) < n_trades:
        is_informed = np.random.random() < pi_informed

        if is_informed:
            true_value = np.random.gamma(shape=K, scale=1.0 / LAMBDA)

            if true_value > ask:
                # El trader informado compra al Ask.
                side = "buy"
                pnl = ask - true_value
                inventory_change = -1

            elif true_value < bid:
                # El trader informado vende al Bid.
                side = "sell"
                pnl = true_value - bid
                inventory_change = 1

            else:
                # No hay oportunidad informada y no se ejecuta.
                continue

        else:
            true_value = np.nan
            side = np.random.choice(["buy", "sell"])

            if side == "buy":
                side_spread = ask - S0
                execution_prob = float(execution_probability(side_spread))

                if np.random.random() > execution_prob:
                    continue

                pnl = ask - S0
                inventory_change = -1

            else:
                side_spread = S0 - bid
                execution_prob = float(execution_probability(side_spread))

                if np.random.random() > execution_prob:
                    continue

                pnl = S0 - bid
                inventory_change = 1

        records.append(
            {
                "trade": len(records) + 1,
                "pnl": pnl,
                "inventory_change": inventory_change,
                "trader_type": (
                    "informed" if is_informed else "liquidity"
                ),
                "side": side,
                "true_value": true_value,
            }
        )

    trades = pd.DataFrame(records)

    trades["cumulative_pnl"] = trades["pnl"].cumsum()
    trades["cumulative_inventory"] = trades["inventory_change"].cumsum()

    return trades

def run_monte_carlo(
    regimes,
    n_runs=1_000,
    trades_per_run=1_000,
    pi_informed=PI_INFORMED,
    base_seed=1_000,
):
    """
    Ejecuta múltiples simulaciones independientes para cada régimen.

    Retorna:
    - Los resultados individuales de cada corrida.
    - Un resumen con media, desviación estándar y probabilidad de pérdida.
    """
    results = []

    for regime_name, quotes in regimes.items():
        bid = quotes["bid"]
        ask = quotes["ask"]

        for run in range(n_runs):
            trades = simulate_trades(
                bid=bid,
                ask=ask,
                n_trades=trades_per_run,
                pi_informed=pi_informed,
                seed=base_seed + run,
            )

            results.append(
                {
                    "regime": regime_name,
                    "run": run + 1,
                    "final_pnl": trades["pnl"].sum(),
                }
            )

    results_df = pd.DataFrame(results)

    summary = (
        results_df.groupby("regime")["final_pnl"]
        .agg(
            mean_pnl="mean",
            std_pnl="std",
            loss_probability=lambda values: (values < 0).mean(),
        )
        .reset_index()
    )

    return results_df, summary