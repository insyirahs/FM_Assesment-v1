import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_csv("demand-forecasting-kernels-only/train.csv")

print(df.head())

df['date'] = pd.to_datetime(df['date'])

df = df.groupby('date')['sales'].sum().reset_index()

df = df.sort_values('date')

df = df.set_index('date')

df = df.ffill()

train = df[:-90]
test = df[-90:]

model = ARIMA(train['sales'], order=(5,1,0))
model_fit = model.fit()

pred = model_fit.forecast(steps=90)

mae = mean_absolute_error(test['sales'], pred)
rmse = np.sqrt(mean_squared_error(test['sales'], pred))
mape = np.mean(np.abs((test['sales'] - pred) / test['sales'])) * 100

print("MAE:", mae)
print("RMSE:", rmse)
print("MAPE:", mape)

plt.figure(figsize=(12,5))
plt.plot(df['sales'], label='Actual')
plt.plot(pred, label='Forecast', color='red')
plt.legend()
plt.title("Sales Forecast")
plt.show()