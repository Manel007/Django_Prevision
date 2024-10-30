from django.shortcuts import render, get_object_or_404, redirect
from .models import Pesticide
from .forms import PesticideForm
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404  
from django.contrib import messages

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")


def all_pesticide(request):
    search_query = request.GET.get('search', '')

    if search_query:
        pesticides = Pesticide.objects.filter(
            Q(domain__icontains=search_query) | 
            Q(area__icontains=search_query) |
            Q(element__icontains=search_query) |
            Q(item__icontains=search_query) |
            Q(year__icontains=search_query) |
            Q(unit__icontains=search_query) |
            Q(value__icontains=search_query)
        )
    else:
        pesticides = Pesticide.objects.all()

    paginator = Paginator(pesticides, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pesticide/all_pesticide.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })
@login_required(login_url="/login/")

def pesticide_create(request):
    if request.method == "POST":
        form = PesticideForm(request.POST)
        
        if form.is_valid():
            area = form.cleaned_data.get('area')
            year = form.cleaned_data.get('year')

            if year and (year < 2017 or year > 2100):
                form.add_error('year', 'L\'année doit être comprise entre 2017 et 2100.')
           
            if not form.errors:
                pesticide = form.save(commit=False)  
                pesticide.value = 0  
                pesticide.save()  
                return redirect('all_pesticide')
    
    else:
        form = PesticideForm()

    return render(request, 'pesticide/create_pesticide.html', {'form': form})
@login_required(login_url="/login/")

def edit_pesticide(request, pk):
    pesticide = get_object_or_404(Pesticide, pk=pk)  
    if request.method == "POST":
        form = PesticideForm(request.POST, instance=pesticide)
        if form.is_valid():
            Area = form.cleaned_data.get('Area')
            Year = form.cleaned_data.get('Year')

            if Year and (Year < 1900 or Year > 2100):
                form.add_error('Year', 'L\'année doit être comprise entre 1900 et 2100.')

            if not form.errors:
                form.save()
                return redirect('all_pesticide')
    else:
        form = PesticideForm(instance=pesticide)
    
    return render(request, 'pesticide/edit_pesticide.html', {'form': form})
@login_required(login_url="/login/")


def delete_pesticide(request, pk):
    pesticide = get_object_or_404(Pesticide, pk=pk)
    if request.method == "POST":
        pesticide.delete()
        return redirect('all_pesticide')
    return render(request, 'pesticide/delete_pesticide.html', {'pesticide': pesticide})
@login_required(login_url="/login/")


def pesticide_prediction_view(request, pesticide_id=None, predict_all=False):
    try:
        data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv')
    except FileNotFoundError:
        return HttpResponse("Le fichier CSV des pesticides est introuvable.")

    if data.empty:
        return HttpResponse("Pas de données disponibles pour la prédiction.")

    data.dropna(inplace=True)

    data.columns = data.columns.str.strip()  
    required_columns = ['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Value']
    
    for column in required_columns:
        if column not in data.columns:
            return HttpResponse(f"La colonne '{column}' est manquante dans les données.")

    X = data[required_columns[:-1]]  
    y = data['Value']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    categorical_features = ['Domain', 'Area', 'Element', 'Item', 'Unit']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[('cat', categorical_transformer, categorical_features)],
        remainder='passthrough'
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    model.fit(X_train, y_train)

    if predict_all:
        predictions = model.predict(X)
        data['Prediction'] = predictions

        page_number = request.GET.get('page', 1)
        paginator = Paginator(data[['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Prediction']].to_dict(orient='records'), 10)
        page_obj = paginator.get_page(page_number)

        context = {
            'all_predictions': page_obj,
            'mse': mean_squared_error(y_test, model.predict(X_test)),
        }

        return render(request, 'pesticide/all_predictions.html', context)

    else:
        pesticide = get_object_or_404(Pesticide, id=pesticide_id)

        new_data = pd.DataFrame([{
            'Domain': pesticide.domain,
            'Area': pesticide.area,
            'Element': pesticide.element,
            'Item': pesticide.item,
            'Year': pesticide.year,
            'Unit': pesticide.unit
        }])

        new_data = new_data.reindex(columns=required_columns[:-1], fill_value=0)

        prediction = model.predict(new_data)[0]

        pesticide.value = prediction
        pesticide.save()  

        context = {
            'prediction': prediction,
            'pesticide': pesticide,
            'mse': mean_squared_error(y_test, model.predict(X_test)),
        }

        return render(request, 'pesticide/prediction_result.html', context)
@login_required(login_url="/login/")

def store_selected_pesticides(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_pesticides')

        if not selected_ids:
            messages.warning(request, 'Aucun pesticide sélectionné.')
            return redirect('all_pesticide')

        try:
            pesticide_data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv')
        except FileNotFoundError:
            pesticide_data = pd.DataFrame(columns=['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Value'])

        for pesticide_id in selected_ids:
            try:
                pesticide = get_object_or_404(Pesticide, id=int(pesticide_id))
                new_row = pd.DataFrame({
                    'Domain': [pesticide.domain],
                    'Area': [pesticide.area],
                    'Element': [pesticide.element],
                    'Item': [pesticide.item],
                    'Year': [pesticide.year],
                    'Unit': [pesticide.unit],
                    'Value': [pesticide.value]
                })
                pesticide_data = pd.concat([pesticide_data, new_row], ignore_index=True)
            except ValueError:
                messages.warning(request, f'ID invalide: {pesticide_id}. L\'ID doit être un entier.')
            except Http404:
                messages.warning(request, f'Le pesticide avec l\'ID {pesticide_id} n\'existe pas.')


        pesticide_data.to_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv', index=False)
        messages.success(request, 'The data of the selected pesticides has been added to the CSV file successfully.')

      

    return render(request, 'pesticide/all_pesticide.html')
@login_required(login_url="/login/")

def all_pesticideFront(request, predict_allF=False):
    try:
        data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv')
    except FileNotFoundError:
        return HttpResponse("Le fichier CSV des pesticides est introuvable.")

    if data.empty:
        return HttpResponse("Pas de données disponibles pour la prédiction.")

    data.dropna(inplace=True)
    data.columns = data.columns.str.strip()
    required_columns = ['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Value']
    
    for column in required_columns:
        if column not in data.columns:
            return HttpResponse(f"La colonne '{column}' est manquante dans les données.")

    X = data[required_columns[:-1]]
    y = data['Value']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    categorical_features = ['Domain', 'Area', 'Element', 'Item', 'Unit']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[('cat', categorical_transformer, categorical_features)],
        remainder='passthrough'
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    model.fit(X_train, y_train)

    if predict_allF:
        predictions = model.predict(X)
        data['Prediction'] = predictions

        search_query = request.GET.get('search', '').strip()
        if search_query:
            data = data[data.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

        page_number = request.GET.get('page', 1)
        paginator = Paginator(data[['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Prediction']].to_dict(orient='records'), 10)
        page_obj = paginator.get_page(page_number)

        context = {
            'all_predictions': page_obj,
            'search_query': search_query,  
            'mse': mean_squared_error(y_test, model.predict(X_test)),
        }

        return render(request, 'pesticide/all_pesticideFront.html', context)
