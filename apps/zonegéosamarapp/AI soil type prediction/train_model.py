from sklearn.tree import DecisionTreeClassifier  # or another classifier
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import os

# Load the dataset
df = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/apps/zonegéosamarapp/AI soil type prediction/soil_analysis_data.csv')

print("Columns in the DataFrame:", df.columns.tolist())

X = df[['pH Level', 'Organic Matter (%)', 'Nitrogen Content (kg/ha)', 
         'Phosphorus Content (kg/ha)', 'Potassium Content (kg/ha)']]
y = df['Soil Type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

model_directory = 'analysis'  # Change as necessary
if not os.path.exists(model_directory):
    os.makedirs(model_directory)

joblib.dump(model, os.path.join(model_directory, 'soil_type_model.pkl'))

print("Model trained and saved successfully!")
