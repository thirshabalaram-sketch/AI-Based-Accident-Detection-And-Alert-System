import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# Load data and model
df = pd.read_csv('data/accident_data.csv')
model = joblib.load('model/severity_model.pkl')

X = df[['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'speed']]
y = df['severity']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preds = model.predict(X_test)

# --- Confusion Matrix ---
cm = confusion_matrix(y_test, preds)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Normal', 'Moderate', 'Severe'],
            yticklabels=['Normal', 'Moderate', 'Severe'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - Severity Prediction')
plt.tight_layout()
plt.savefig('model/confusion_matrix.png', dpi=150)
plt.close()

# --- Feature Importance ---
importances = model.feature_importances_
feature_names = X.columns
plt.figure(figsize=(7, 5))
sns.barplot(x=importances, y=feature_names, hue=feature_names, palette='viridis', legend=False)
plt.xlabel('Importance Score')
plt.title('Feature Importance - Severity Classifier')
plt.tight_layout()
plt.savefig('model/feature_importance.png', dpi=150)
plt.close()

print("Saved: model/confusion_matrix.png")
print("Saved: model/feature_importance.png")