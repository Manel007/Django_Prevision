import joblib
import pandas as pd


model = joblib.load('trained_model.pkl')



data_test = pd.DataFrame({
    'cycle_croissance_jours': [30, 60],  
    'rendement_attendu': [1000, 2000]    
})

try:
    predictions = model.predict(data_test)
    print("Recommendation :", predictions)
except ValueError as e:
    print(f"Erreur de recommendation : {e}")
