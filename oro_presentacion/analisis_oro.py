"""Caso académico: recuperación de oro. Resultados pendientes de ejecución real."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import make_scorer

TARGETS = ['rougher.output.recovery', 'final.output.recovery']

def smape(y_true, y_pred):
    actual, predicted = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    if actual.shape != predicted.shape or actual.size == 0:
        raise ValueError('Se requieren arreglos no vacíos con la misma forma.')
    if not np.isfinite(actual).all() or not np.isfinite(predicted).all():
        raise ValueError('sMAPE requiere valores finitos.')
    denominator = np.abs(actual) + np.abs(predicted)
    # Convención explícita: el par (0,0) aporta cero al error.
    terms = np.divide(2 * np.abs(predicted - actual), denominator,
                      out=np.zeros_like(actual), where=denominator != 0)
    return float(100 * terms.mean())

def weighted_smape(y_true, y_pred):
    actual, predicted = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    if actual.ndim != 2 or actual.shape[1] != 2 or actual.shape != predicted.shape:
        raise ValueError('Orden requerido de objetivos: rougher y final, dos columnas.')
    return .25 * smape(actual[:, 0], predicted[:, 0]) + .75 * smape(actual[:, 1], predicted[:, 1])

SCORER = make_scorer(weighted_smape, greater_is_better=False)

def read_table(path):
    data = pd.read_csv(Path(path))
    if 'date' not in data:
        raise ValueError('Falta la clave temporal date.')
    data['date'] = pd.to_datetime(data['date'], errors='raise')
    if data['date'].isna().any() or data['date'].duplicated().any():
        raise ValueError('Revisar fechas ausentes o repetidas antes de asociar resultados.')
    return data.sort_values('date').reset_index(drop=True)

def observed_targets(data):
    values = data[TARGETS].to_numpy(dtype=float)
    return np.isfinite(values).all(axis=1) & ((values >= 0) & (values <= 100)).all(axis=1)

def prepare_training(train, test_schema):
    # El esquema de prueba define disponibilidad; no sus distribuciones ni resultados.
    candidates = [c for c in test_schema.columns if c != 'date']
    forbidden = [c for c in candidates if c in TARGETS or '.output.' in c or '.calculation.' in c
                 or c == 'calculated_recovery']
    if forbidden:
        raise ValueError(f'Revisar variables de salida o derivadas: {forbidden}')
    if not candidates or not set(candidates).issubset(train.columns):
        raise ValueError('No hay un esquema de predicción compatible.')
    if not all(pd.api.types.is_numeric_dtype(train[c]) for c in candidates):
        raise ValueError('Revisar tipos no numéricos en los predictores.')
    valid = observed_targets(train)
    clean = train.loc[valid].sort_values('date').reset_index(drop=True)
    if len(clean) < 12:
        raise ValueError('Muy pocas observaciones etiquetadas para la validación temporal.')
    X = clean[candidates].replace([np.inf, -np.inf], np.nan)
    if X.isna().all().any():
        raise ValueError('Hay predictores sin observaciones en todo el entrenamiento.')
    return X, clean[TARGETS], candidates, {'total_train':len(train), 'evaluables_train':len(clean),
                                         'excluidos_objetivo':int((~valid).sum())}

def model_candidates():
    estimators = {
        'Referencia (media)': DummyRegressor(strategy='mean'),
        'Regresión lineal': LinearRegression(),
        'Árbol de decisión': DecisionTreeRegressor(max_depth=6, min_samples_leaf=10, random_state=42),
        'Bosque aleatorio': RandomForestRegressor(n_estimators=100, max_depth=8,
                                                  min_samples_leaf=5, random_state=42, n_jobs=-1),
    }
    return {name: Pipeline([('imputer',SimpleImputer(strategy='median')),
                            ('scaler',StandardScaler()), ('model',estimator)])
            for name,estimator in estimators.items()}

def compare_models(X, y, n_splits=5):
    models, rows = model_candidates(), []
    # Orden temporal de X/y establecido en prepare_training; no barajar.
    cv = TimeSeriesSplit(n_splits=n_splits)
    for name, model in models.items():
        losses = -cross_val_score(model, X, y, cv=cv, scoring=SCORER, error_score='raise')
        rows.append({'modelo':name, 'sMAPE_CV':float(losses.mean()),
                     'desviacion_entre_particiones':float(losses.std(ddof=1))})
    scores = pd.DataFrame(rows).set_index('modelo').sort_values('sMAPE_CV')
    return models, scores

def evaluate_reserved(model, X_train, y_train, test, full, features):
    # full se usa exclusivamente para recuperar etiquetas de prueba por fecha.
    labels = full[['date', *TARGETS]]
    overlap = test['date'].isin(full['date'])
    if not overlap.all():
        raise ValueError('Hay fechas de prueba sin correspondencia en full.')
    if set(features) - set(test.columns):
        raise ValueError('Faltan predictores en prueba.')
    merged = test[['date', *features]].merge(labels, on='date', how='left', validate='one_to_one')
    valid = observed_targets(merged)
    if not valid.any():
        raise ValueError('No hay objetivos de prueba observados y válidos.')
    model.fit(X_train, y_train)
    X_test = merged[features].replace([np.inf, -np.inf], np.nan)
    prediction = model.predict(X_test)
    real = merged.loc[valid,TARGETS].to_numpy()
    pred_valid = prediction[valid]
    metrics = {'sMAPE_rougher':smape(real[:,0],pred_valid[:,0]),
               'sMAPE_final':smape(real[:,1],pred_valid[:,1]),
               'sMAPE_ponderado':weighted_smape(real,pred_valid),
               'total_test':len(test), 'evaluables_test':int(valid.sum()),
               'sin_objetivo_valido':int((~valid).sum()),
               'predicciones_fuera_0_100':int(((prediction < 0) | (prediction > 100)).any(axis=1).sum())}
    result = merged[['date']].copy()
    result[['pred_rougher','pred_final']] = prediction
    return metrics, result

def recovery_diagnostic(train):
    cols = ['rougher.output.concentrate_au','rougher.input.feed_au',
            'rougher.output.tail_au','rougher.output.recovery']
    a = train[cols].to_numpy(dtype=float)
    C,F,T,actual = a.T
    denominator = F * (C-T)
    valid = np.isfinite(a).all(axis=1) & (denominator != 0) & (C >= F) & (F >= T) & (T >= 0)
    valid &= (actual >= 0) & (actual <= 100)
    calculated = np.full(len(a),np.nan)
    calculated[valid] = 100 * C[valid] * (F[valid]-T[valid]) / denominator[valid]
    finite = valid & np.isfinite(calculated)
    return {'filas':len(a), 'comparables':int(finite.sum()),
            'no_comparables':int((~finite).sum()),
            'MAE_formula':float(np.abs(actual[finite]-calculated[finite]).mean()) if finite.any() else None}
