import pandas as pd

file_path = 'techniques.csv'  

df = pd.read_csv(file_path)

print(df.head())

print(df.columns)