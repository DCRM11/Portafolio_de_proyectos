"""Evaluación académica; no constituye una evaluación de reservas certificada."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

FEATURES = ['f0', 'f1', 'f2']
BUDGET = 100_000_000
UNIT_REVENUE = 4_500
N_WELLS = 200

def load_region(path):
    data = pd.read_csv(Path(path))
    required = ['id', *FEATURES, 'product']
    if not set(required).issubset(data.columns):
        raise ValueError(f'Faltan columnas en {path}: {set(required)-set(data.columns)}')
    if data[required].isna().any().any():
        raise ValueError('Revisar valores ausentes antes de entrenar.')
    if not np.isfinite(data[FEATURES + ['product']].to_numpy(dtype=float)).all():
        raise ValueError('Valores no finitos en variables numéricas.')
    if (data['product'] < 0).any():
        raise ValueError('El volumen real no puede ser negativo.')
    # No se eliminan registros automáticamente: un ID repetido exige revisión.
    if data['id'].duplicated().any():
        raise ValueError('Hay identificadores repetidos: revisar su significado y definir agrupación o depuración antes de dividir.')
    return data

def fit_region(data):
    train, valid = train_test_split(data, test_size=0.25, random_state=42)
    model = LinearRegression().fit(train[FEATURES], train['product'])
    pred = model.predict(valid[FEATURES])
    pairs = pd.DataFrame({'actual':valid['product'].to_numpy(), 'predicted':pred})
    metrics = {'mean_predicted':float(pred.mean()),
               'rmse':float(np.sqrt(mean_squared_error(pairs.actual, pred)))}
    return model, pairs, metrics

def profit(pairs, n_wells=N_WELLS, budget=BUDGET, unit_revenue=UNIT_REVENUE):
    if n_wells <= 0 or len(pairs) < n_wells:
        raise ValueError('La muestra debe contener al menos el número de pozos a seleccionar.')
    if not np.isfinite(pairs[['actual','predicted']].to_numpy()).all():
        raise ValueError('Valores no finitos en pares de evaluación.')
    # Predicciones deciden el orden; observaciones reales evalúan el resultado.
    selected = pairs.sort_values('predicted', ascending=False, kind='stable').head(n_wells)
    return float(selected.actual.sum() * unit_revenue - budget)

def bootstrap_profit(pairs, candidates, n_boot=1000, seed=42, n_wells=N_WELLS):
    if not isinstance(candidates, (int, np.integer)) or not n_wells <= candidates <= len(pairs):
        raise ValueError('Confirma candidatos: entero entre pozos seleccionados y tamaño de validación.')
    if n_boot < 2:
        raise ValueError('Se necesitan al menos dos réplicas.')
    rng = np.random.default_rng(seed)
    # Se remuestrean filas completas para mantener alineados predicción y valor real.
    values = np.array([profit(pairs.iloc[rng.integers(0, len(pairs), size=candidates)], n_wells=n_wells)
                       for _ in range(n_boot)])
    return values

def summarize(values):
    return {'mean_profit_usd':float(np.mean(values)),
            'p025_usd':float(np.quantile(values, 0.025)),
            'p975_usd':float(np.quantile(values, 0.975)),
            'loss_probability':float(np.mean(values < 0))}
