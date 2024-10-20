# apps/authentication/views.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from .forms import TemperaturePredictionForm  # Importez le formulaire que vous avez créé
from .models import YieldData

from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from .models import Culture  # Adjust import according to your model's location
from django.http import JsonResponse
from .forms import CultureForm  # Assuming you have a form for Culture
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # Uncomment the following line if you want to redirect to the login page after registration
            # return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def culture_list(request):
    cultures = Culture.objects.all()
    return render(request, 'home/culture_list.html', {'cultures': cultures})

def culture_create(request):
    if request.method == "POST":
        # Retrieve form data
        nom = request.POST.get('nom')
        type_culture = request.POST.get('type_culture')
        duree_croissance = request.POST.get('duree_croissance')
        superficie_requise = request.POST.get('superficie_requise')
        conditions_optimales = request.POST.get('conditions_optimales')

        # Create a new culture if all fields are provided
        if all([nom, type_culture, duree_croissance, superficie_requise, conditions_optimales]):
            Culture.objects.create(
                nom=nom,
                type_culture=type_culture,
                duree_croissance=duree_croissance,
                superficie_requise=superficie_requise,
                conditions_optimales=conditions_optimales
            )
            return redirect('culture_list')  # Redirect to the culture list after creation
        else:
            msg = "Please fill in all fields."  # Error message for incomplete form
        
    return render(request, 'home/culture_form.html')  # Render the form
def culture_update(request, culture_id):  # Use 'culture_id' here
    culture = get_object_or_404(Culture, id=culture_id)

    if request.method == 'POST':
        culture.nom = request.POST.get('nom')
        culture.type_culture = request.POST.get('type_culture')
        culture.duree_croissance = request.POST.get('duree_croissance')
        culture.superficie_requise = request.POST.get('superficie_requise')
        culture.conditions_optimales = request.POST.get('conditions_optimales')
        culture.save()
        return redirect('culture_list')

    return render(request, 'home/culture_form.html', {'culture': culture})


def culture_delete(request, culture_id):
    culture = get_object_or_404(Culture, id=culture_id)
    print("Attempting to delete culture:", culture.nom)

    if request.method == 'POST':
        culture.delete()
        print("Culture deleted.")
        return JsonResponse({'success': True})

    return render(request, 'home/culture_confirm_delete.html', {'culture': culture})



# Modéle 1 linéar regressionn  Ikraaaaaaaaam !

df = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/yield_df.csv')  # Adjust the path to your CSV file

def predict_yield(request):
    predicted_yield = None  # Initialize the variable for predicted yield
    if request.method == 'POST':
        # Get data from the form
        average_rainfall = float(request.POST.get('average_rainfall', 0))
        pesticides_used = float(request.POST.get('pesticides_used', 0))
        avg_temp = float(request.POST.get('avg_temp', 0))

        # Prepare input for the model
        input_data = pd.DataFrame([[average_rainfall, pesticides_used, avg_temp]],
                                   columns=['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'])

        # Select features and target variable for the entire dataset
        X = df[['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
        y = df['hg/ha_yield']

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        predicted_yield = model.predict(input_data)[0]

    return render(request, 'yield_prediction.html', {'predicted_yield': predicted_yield})
   



   #modéle222 RandomForestRegressor  Ikraaaaaaaaam !
def temperature_prediction_view(request):
    prediction = None
    mse = None  # Pour afficher l'erreur quadratique moyenne si nécessaire
    if request.method == 'POST':
        form = TemperaturePredictionForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']

            # Charger les données du CSV
            df_temp = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/temp.csv')
            df_temp['avg_temp'] = df_temp['avg_temp'].replace(np.nan, df_temp['avg_temp'].mean())
            df_temp['year'] = df_temp['year'].astype(int)

            # Préparer les données pour le modèle
            X = df_temp[['year']]
            y = df_temp['avg_temp']

            # Diviser les données en ensembles d'entraînement et de test
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Créer le modèle de forêt aléatoire
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Faire des prédictions pour l'année donnée
            prediction = model.predict([[year]])[0]

            # Calculer la performance du modèle (facultatif)
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)

    else:
        form = TemperaturePredictionForm()

    return render(request, 'temperature_prediction.html', {
        'form': form,
        'prediction': prediction,
        'mse': mse,
    })

def pre_yield(request):
    if request.method == 'POST':
        # Get data from request
        average_rainfall = float(request.POST.get('average_rainfall'))
        pesticides_used = float(request.POST.get('pesticides_used'))
        avg_temp = float(request.POST.get('avg_temp'))

        # Load the trained model
        model = joblib.load('model.pkl')

        # Make prediction
        prediction = model.predict(np.array([[average_rainfall, pesticides_used, avg_temp]]))
        
        # Return the prediction
        return JsonResponse({'predicted_yield': prediction[0]})

    return render(request, 'predict_yield.html')  