import joblib
import pandas as pd

model_path = 'apps/zonegéosamarapp/AI soil type prediction/soil_type_model.pkl'  
model = joblib.load(model_path)


def predict_soil_type(pH_level, organic_matter, nitrogen_content, phosphorus_content, potassium_content):
    input_data = pd.DataFrame({
        'pH Level': [pH_level],
        'Organic Matter (%)': [organic_matter],
        'Nitrogen Content (kg/ha)': [nitrogen_content],
        'Phosphorus Content (kg/ha)': [phosphorus_content],
        'Potassium Content (kg/ha)': [potassium_content]
    })

    predicted_soil_type = model.predict(input_data)
    return predicted_soil_type[0]
