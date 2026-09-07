# Laboratorio 01: Cotizaciones óptimas de un market maker

- Erik del Castillo

## Descripción

Este proyecto implementa el modelo de Copeland y Galai (1983) para determinar las cotizaciones Bid y Ask que maximizan la utilidad esperada de un formador de mercado. El modelo considera las ganancias obtenidas frente a traders de liquidez y las pérdidas provocadas por traders informados. Además, compara tres regímenes de cotización mediante simulaciones de 10,000 trades y un análisis Monte Carlo de 1,000 corridas independientes.

## Estructura del proyecto

```text
Lab01_FinanzasCuantitativas_EquipoN/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── src/
│   ├── model.py
│   ├── simulation.py
│   └── plots.py
├── tests/
│   └── test_model.py
├── notebooks/
│   └── analysis.ipynb
└── docs/
    ├── figures/
    └── presentacion.pdf
```

## Instalación

Se requiere Python 3.12 o una versión compatible.

Crear el ambiente virtual:

```bash
python -m venv venv
```

Activarlo en Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Reproducción de resultados

Para ejecutar la optimización, las simulaciones, el análisis Monte Carlo, el análisis de sensibilidad y generar todas las figuras:

```bash
python main.py
```

Para ejecutar las pruebas automáticas:

```bash
python -m pytest -v
```

La semilla aleatoria utilizada es `42`. Se encuentra definida en `main.py` y se proporciona explícitamente a las funciones de simulación para obtener resultados reproducibles.

## Parámetros del caso base

| Parámetro | Valor |
|---|---:|
| Precio de referencia | 19.90 |
| Distribución del valor verdadero | Erlang(60, 3) |
| Probabilidad de trader informado | 0.40 |
| Probabilidad de trader de liquidez | 0.60 |
| Probabilidad de ejecución | max(0, 0.50 - 0.08s) |

## Resultados de la optimización

| Resultado | Valor |
|---|---:|
| Bid óptimo | 16.45 |
| Ask óptimo | 23.43 |
| Spread óptimo | 6.98 |
| Utilidad esperada por llegada | 0.84 |

## Simulación de 10,000 trades

| Régimen | P&L final | Inventario final | Máximo desbalance |
|---|---:|---:|---:|
| Óptimo | 18,526.93 | -246 | 289 |
| Estrecho | -10,703.64 | -110 | 156 |
| Amplio | -144.00 | -264 | 267 |

## Resultados de Monte Carlo

Cada régimen se evaluó mediante 1,000 corridas independientes de 1,000 trades.

| Régimen | P&L promedio | Desviación estándar | Probabilidad de pérdida |
|---|---:|---:|---:|
| Óptimo | 1,866.44 | 72.27 | 0.0% |
| Estrecho | -1,067.19 | 49.58 | 100.0% |
| Amplio | -35.23 | 56.50 | 74.4% |

## Análisis de sensibilidad

| Probabilidad informada | Bid | Ask | Spread | Utilidad esperada |
|---:|---:|---:|---:|---:|
| 0.10 | 16.71 | 23.11 | 6.40 | 1.38 |
| 0.40 | 16.45 | 23.43 | 6.98 | 0.84 |
| 0.70 | 16.01 | 24.00 | 7.99 | 0.34 |

El spread óptimo aumenta conforme se incrementa la proporción de traders informados. Este comportamiento coincide con la teoría: una mayor exposición a selección adversa obliga al formador de mercado a exigir una compensación mayor.

## Preguntas de análisis

### 1. ¿Por qué los traders informados generan la necesidad de un spread?

En el régimen estrecho, el formador de mercado obtuvo una ganancia de 657.00 frente a traders de liquidez, pero sufrió una pérdida de 11,360.64 frente a traders informados. El resultado fue un P&L total de -10,703.64. Por lo tanto, un spread de 0.30 no proporciona ingresos suficientes para compensar el costo de selección adversa.

### 2. ¿Cómo cambia el costo de selección adversa conforme se amplía el spread?

La pérdida frente a traders informados fue de 11,360.64 en el régimen estrecho, 7,777.50 en el amplio y 4,265.27 en el óptimo. La magnitud de la pérdida disminuye conforme las cotizaciones se alejan del precio de referencia, ya que se reducen las oportunidades rentables disponibles para los traders informados.

### 3. ¿Cuál régimen acumula el mayor desbalance de inventario?

En la trayectoria simulada, el régimen óptimo alcanzó el mayor desbalance absoluto, con 289 unidades. El régimen amplio alcanzó 267 y el estrecho 156. Este resultado depende de la secuencia aleatoria de operaciones y no implica que el régimen óptimo siempre acumule más inventario.

En un mercado real, mantener una posición desbalanceada expone al formador de mercado al riesgo de movimientos posteriores del precio. El modelo no captura ese riesgo porque utiliza un precio de referencia fijo y no ajusta las cotizaciones en función del inventario.

### 4. ¿Cómo se comporta el spread óptimo al variar la proporción informada?

El spread óptimo aumentó de 6.40 con una proporción informada de 10%, a 6.98 con 40% y a 7.99 con 70%. El resultado coincide con la predicción teórica de que una mayor presencia de información privada requiere cotizaciones más amplias.

### 5. ¿Cuáles son tres limitaciones del modelo?

1. El precio de referencia permanece fijo durante toda la simulación.
2. El modelo no penaliza el inventario ni ajusta dinámicamente las cotizaciones.
3. No considera comisiones, latencia, competencia, prioridad de órdenes ni otros elementos reales del mercado.

Adicionalmente, la simulación completa un número fijo de trades ejecutados. Por ello, los resultados representan rentabilidad por trade y no rentabilidad por unidad de tiempo. Un spread amplio puede verse favorecido bajo esta métrica, aunque en un mercado real sus operaciones podrían tardar más en ejecutarse.

## Nota técnica sobre el caso sin traders informados

Con una ganancia por lado igual a:

```text
g(s) = (0.50 - 0.08s)s
```

la condición de primer orden es:

```text
g'(s) = 0.50 - 0.16s = 0
```

Por lo tanto, el máximo ocurre en `s = 3.125`. El valor `6.25 = 0.50 / 0.08` indicado en los lineamientos corresponde al punto donde la probabilidad de ejecución llega a cero, no al máximo de la ganancia.

## Uso de inteligencia artificial

Se utilizó asistencia de inteligencia artificial para orientar la estructura modular del proyecto, revisar la implementación en Python, apoyar la detección de errores y mejorar la documentación. Todas las funciones, supuestos, resultados y conclusiones fueron revisados por los integrantes, quienes son responsables de comprender y explicar el código entregado.