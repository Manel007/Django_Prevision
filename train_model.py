import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Chargez les données de pluie
df = pd.read_csv('rainfall.csv')

# Filtrer les données pour l'Afghanistan
df = df[df['Area'] == 'Afghanistan']

# Vérifiez les types de données
print(df['average_rain_fall_mm_per_year'].dtype)

# Affichez les valeurs uniques dans la colonne
print("Valeurs uniques dans 'average_rain_fall_mm_per_year':")
print(df['average_rain_fall_mm_per_year'].unique())

# Convertir la colonne en numérique, en remplaçant les erreurs par NaN
df['average_rain_fall_mm_per_year'] = pd.to_numeric(df['average_rain_fall_mm_per_year'], errors='coerce')

# Supprimez les lignes contenant des NaN
df.dropna(subset=['average_rain_fall_mm_per_year'], inplace=True)

# Remplir les valeurs manquantes avec la moyenne
df['average_rain_fall_mm_per_year'] = df['average_rain_fall_mm_per_year'].fillna(df['average_rain_fall_mm_per_year'].mean())

# Sélectionnez les colonnes pertinentes
data = df[['Year', 'average_rain_fall_mm_per_year']]

# Tracez les données pour visualiser
plt.plot(data['Year'], data['average_rain_fall_mm_per_year'])
plt.xlabel('Année')
plt.ylabel('Pluviométrie moyenne (mm)')
plt.title('Pluviométrie moyenne au fil des ans en Afghanistan')
plt.show()

# Normalisez les données de pluie
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data[['average_rain_fall_mm_per_year']])

# Préparez les séquences (3 années précédentes pour prédire la suivante)
time_step = 3
X, y = [], []
for i in range(len(data_scaled) - time_step):
    X.append(data_scaled[i:i + time_step])
    y.append(data_scaled[i + time_step])

X = np.array(X)
y = np.array(y)

# Divisez les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Calculez le pourcentage d'entraînement et de test
train_size = len(X_train)
test_size = len(X_test)
total_size = train_size + test_size

train_percentage = (train_size / total_size) * 100
test_percentage = (test_size / total_size) * 100

print(f"Taille de l'ensemble d'entraînement : {train_size} ({train_percentage:.2f}%)")
print(f"Taille de l'ensemble de test : {test_size} ({test_percentage:.2f}%)")

# --- Modèle LSTM ---
# Construisez le modèle LSTM avec dropout
model = Sequential()
model.add(LSTM(100, return_sequences=True, input_shape=(time_step, 1)))
model.add(Dropout(0.2))  # Dropout pour régularisation
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(1))  # Une sortie pour prédire la pluie

# Compilez le modèle
model.compile(optimizer='adam', loss='mean_squared_error')

# Entraînez le modèle
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# Sauvegardez le modèle entraîné
model.save('rainfall_prediction_rnn.keras')

# --- Modèle de Régression Linéaire ---
# Pour la régression linéaire, nous devons reformater les données
X_linear = data[['Year']].values  # Utiliser seulement l'année comme caractéristique
y_linear = data['average_rain_fall_mm_per_year'].values

# Divisez les données en ensembles d'entraînement et de test pour la régression linéaire
X_train_linear, X_test_linear, y_train_linear, y_test_linear = train_test_split(X_linear, y_linear, test_size=0.2, random_state=42)

# Créez et entraînez le modèle de régression linéaire
linear_model = LinearRegression()
linear_model.fit(X_train_linear, y_train_linear)

# Prédisez les valeurs de l'ensemble de test
y_pred_linear = linear_model.predict(X_test_linear)

# Évaluez les performances
mse_linear = mean_squared_error(y_test_linear, y_pred_linear)
r2_linear = r2_score(y_test_linear, y_pred_linear)

print(f"Performance du modèle de régression linéaire:")
print(f"MSE: {mse_linear}")
print(f"R^2: {r2_linear}")

# Visualisez les résultats
plt.scatter(X_test_linear, y_test_linear, color='blue', label='Valeurs réelles')
plt.plot(X_test_linear, y_pred_linear, color='red', label='Prédictions (Régression Linéaire)')
plt.xlabel('Année')
plt.ylabel('Pluviométrie moyenne (mm)')
plt.title('Régression Linéaire de la Pluviométrie')
plt.legend()
plt.show()
from sklearn.metrics import mean_squared_error, r2_score

# Supposons que vous ayez vos données y_test et y_pred
y_pred = model.predict(X_test)

# Calcul des métriques
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'MSE: {mse}')
print(f'R²: {r2}')
