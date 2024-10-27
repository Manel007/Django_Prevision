import pandas as pd
from sklearn.ensemble import IsolationForest
from apps.zonegéosamarapp.models import TypeDeSol

def detect_anomalies(new_entry=None):
    # Retrieve dataset and encode
    df = pd.DataFrame(TypeDeSol.objects.values(
        'texture', 'profondeur', 'pH', 'capacite_retenue_eau', 'nutriments_disponibles'
    ))
    df_encoded = pd.get_dummies(df, drop_first=True)

    # Fit Isolation Forest model
    model = IsolationForest(contamination=0.1).fit(df_encoded)

    if new_entry:
        # Prepare new entry for anomaly detection
        new_entry_df = pd.DataFrame([new_entry])
        new_entry_df = pd.get_dummies(new_entry_df, drop_first=True).reindex(columns=df_encoded.columns, fill_value=0)
        
        # Return True if anomaly detected, otherwise False
        return model.predict(new_entry_df)[0] == -1
    
    # Detect anomalies in the entire dataset
    df['anomaly'] = model.predict(df_encoded)

    # Add a name to each anomaly
    anomalies = df[df['anomaly'] == -1].copy()
    anomalies['name'] = [f"Anomaly {i+1}" for i in range(len(anomalies))]
    
     # Count the number of anomalies found
    anomaly_count = len(anomalies)

    return {
        'anomalies': anomalies.to_dict('records'),
        'count': anomaly_count
    }
