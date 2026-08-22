import numpy as np
import pandas as pd

np.random.seed(42)
n_normal = 800
n_accident = 200

normal = pd.DataFrame({
    'accel_x': np.random.normal(0, 0.3, n_normal),
    'accel_y': np.random.normal(0, 0.3, n_normal),
    'accel_z': np.random.normal(9.8, 0.3, n_normal),
    'gyro_x': np.random.normal(0, 5, n_normal),
    'gyro_y': np.random.normal(0, 5, n_normal),
    'gyro_z': np.random.normal(0, 5, n_normal),
    'speed': np.random.uniform(20, 80, n_normal),
    'severity': 0
})

severity_levels = np.random.choice([1, 2], n_accident)
accident = pd.DataFrame({
    'accel_x': np.random.normal(0, 4, n_accident) * severity_levels,
    'accel_y': np.random.normal(0, 4, n_accident) * severity_levels,
    'accel_z': np.random.normal(9.8, 6, n_accident) * severity_levels,
    'gyro_x': np.random.normal(0, 60, n_accident) * severity_levels,
    'gyro_y': np.random.normal(0, 60, n_accident) * severity_levels,
    'gyro_z': np.random.normal(0, 60, n_accident) * severity_levels,
    'speed': np.random.uniform(40, 120, n_accident),
    'severity': severity_levels
})

df = pd.concat([normal, accident], ignore_index=True).sample(frac=1).reset_index(drop=True)
df.to_csv('data/accident_data.csv', index=False)

print("Dataset created successfully!")
print(df['severity'].value_counts())
print(df.head())