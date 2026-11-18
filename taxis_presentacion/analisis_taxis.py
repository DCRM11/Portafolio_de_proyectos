"""Pronóstico académico de pedidos: una hora adelante, con historia actualizada."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, make_scorer

LAGS = (1, 2, 3, 6, 12, 24)
WINDOWS = (24, 168)

def rmse(actual, predicted):
    return float(np.sqrt(mean_squared_error(actual, predicted)))

SCORER = make_scorer(rmse, greater_is_better=False)

def load_hourly(path):
    data = pd.read_csv(Path(path), index_col=0, parse_dates=[0])
    if not isinstance(data.index, pd.DatetimeIndex) or data.index.hasnans:
        raise ValueError('Se requiere un índice de fechas válido.')
    if data.index.duplicated().any():
        raise ValueError('Hay fechas repetidas; revisar antes de agregar.')
    if 'num_orders' not in data:
        raise ValueError('Falta num_orders.')
    data = data.sort_index()
    expected = pd.date_range(data.index.min(), data.index.max(), freq='10min')
    if not data.index.equals(expected):
        raise ValueError('Revisar intervalos: se esperan observaciones cada 10 minutos, sin huecos.')
    y = pd.to_numeric(data['num_orders'], errors='raise')
    if not np.isfinite(y).all() or (y < 0).any() or (y % 1 != 0).any():
        raise ValueError('Los pedidos deben ser conteos no negativos y finitos.')
    counts = y.resample('1h').count()
    if not counts.eq(6).all():
        raise ValueError('Hay horas incompletas; no se rellenan silenciosamente con cero.')
    hourly = y.resample('1h').sum().rename('num_orders')
    return hourly

def make_features(hourly):
    if not hourly.index.is_monotonic_increasing or hourly.index.duplicated().any():
        raise ValueError('La serie debe estar ordenada y sin fechas repetidas.')
    if len(hourly) < 2 or not hourly.index.to_series().diff().iloc[1:].eq(pd.Timedelta(hours=1)).all():
        raise ValueError('Se requiere frecuencia horaria continua.')
    if not np.isfinite(hourly.to_numpy()).all():
        raise ValueError('No se imputan pedidos desconocidos.')
    X = pd.DataFrame(index=hourly.index)
    X['hour'] = hourly.index.hour
    X['dayofweek'] = hourly.index.dayofweek
    for lag in LAGS:
        X[f'lag_{lag}h'] = hourly.shift(lag)
    for window in WINDOWS:
        X[f'rolling_{window}h'] = hourly.shift(1).rolling(window, min_periods=window).mean()
    # Solo se eliminan las filas iniciales sin historia suficiente.
    valid = X.notna().all(axis=1)
    return X.loc[valid], hourly.loc[valid]

def chronological_split(hourly, test_fraction=.1):
    if not 0 < test_fraction < 1:
        raise ValueError('La proporción de prueba debe estar entre cero y uno.')
    n_test = int(np.ceil(len(hourly) * test_fraction))
    if n_test < 2 or n_test >= len(hourly):
        raise ValueError('Serie insuficiente para reservar prueba.')
    cutoff = hourly.index[-n_test]
    X,y = make_features(hourly)
    train_mask = X.index < cutoff
    if train_mask.sum() < 30 or (~train_mask).sum() < 2:
        raise ValueError('Historia insuficiente tras construir variables.')
    return X.loc[train_mask],X.loc[~train_mask],y.loc[train_mask],y.loc[~train_mask],cutoff

def model_candidates():
    return {
        'Regresión lineal': Pipeline([('scale',StandardScaler()),('model',LinearRegression())]),
        'Árbol de decisión': DecisionTreeRegressor(max_depth=8,min_samples_leaf=10,random_state=42),
        'Bosque aleatorio': RandomForestRegressor(n_estimators=100,max_depth=12,
                                                  min_samples_leaf=5,random_state=42,n_jobs=-1),
        'Boosting de histogramas': HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=15,
                                                                early_stopping=False,random_state=42),
    }

def compare_models(X,y,n_splits=5):
    models,rows = model_candidates(),[]
    splitter = TimeSeriesSplit(n_splits=n_splits)
    # Los retardos de cada fecha solo usan observaciones anteriores, incluidas las
    # de validación ya reveladas: evaluación secuencial de un paso, no multihorizonte.
    for name,model in models.items():
        values = -cross_val_score(model,X,y,cv=splitter,scoring=SCORER,error_score='raise')
        rows.append({'modelo':name,'RMSE_CV':float(values.mean()),
                     'desviacion_entre_particiones':float(values.std(ddof=1))})
    for label,column in [('Persistencia última hora','lag_1h'),('Referencia diaria','lag_24h')]:
        values = [rmse(y.iloc[valid],X.iloc[valid][column]) for _,valid in splitter.split(X)]
        rows.append({'modelo':label,'RMSE_CV':float(np.mean(values)),
                     'desviacion_entre_particiones':float(np.std(values,ddof=1))})
    return models,pd.DataFrame(rows).set_index('modelo').sort_values('RMSE_CV')

def evaluate_reserved(selected,models,X_train,y_train,X_test,y_test):
    if X_train.index.max() >= X_test.index.min():
        raise ValueError('La prueba debe ser posterior al entrenamiento.')
    predictions = {'Persistencia última hora':X_test['lag_1h'].to_numpy(),
                   'Referencia diaria':X_test['lag_24h'].to_numpy()}
    if selected in models:
        model = models[selected]
        model.fit(X_train,y_train)
        predictions[selected] = model.predict(X_test)
    elif selected not in predictions:
        raise ValueError('Modelo seleccionado desconocido.')
    rows=[]
    for name,pred in predictions.items():
        rows.append({'modelo':name,'RMSE':rmse(y_test,pred),
                     'MAE':float(mean_absolute_error(y_test,pred)),
                     'R2':float(r2_score(y_test,pred)),
                     'predicciones_negativas':int((np.asarray(pred)<0).sum())})
    prediction_table=pd.DataFrame(predictions,index=y_test.index)
    prediction_table.insert(0,'Observado',y_test)
    return pd.DataFrame(rows).set_index('modelo'),prediction_table
