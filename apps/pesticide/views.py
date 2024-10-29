from django.shortcuts import render, get_object_or_404, redirect
from .models import Pesticide
from .forms import PesticideForm
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404  # Import pour Http404
from django.contrib import messages

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from django.http import HttpResponse


def all_pesticide(request):
    # Récupérer la requête de recherche
    search_query = request.GET.get('search', '')

    # Filtrer les pesticides en fonction de la requête de recherche
    if search_query:
        pesticides = Pesticide.objects.filter(
            Q(Domain__icontains=search_query) | 
            Q(Area__icontains=search_query) |
            Q(element__icontains=search_query) |
            Q(item__icontains=search_query) |
            Q(Year__icontains=search_query) |
            Q(unit__icontains=search_query) |
            Q(value__icontains=search_query)
        )
    else:
        pesticides = Pesticide.objects.all()

    # Pagination - 10 résultats par page
    paginator = Paginator(pesticides, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Rendre le template avec les objets paginés et la requête de recherche
    return render(request, 'pesticide/all_pesticide.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

def pesticide_create(request):
    if request.method == "POST":
        form = PesticideForm(request.POST)
        
        # Vérifier si les données du formulaire sont valides
        if form.is_valid():
            area = form.cleaned_data.get('area')
            year = form.cleaned_data.get('year')

            # Vérification de l'année
            if year and (year < 2017 or year > 2100):
                form.add_error('year', 'L\'année doit être comprise entre 2017 et 2100.')
           
            # Si pas d'erreurs personnalisées, sauvegarder le formulaire
            if not form.errors:
                pesticide = form.save(commit=False)  # Crée l'instance mais ne l'enregistre pas encore
                pesticide.value = 0  # Initialiser la valeur par défaut à 0
                pesticide.save()  # Sauvegarder l'instance dans la base de données
                return redirect('all_pesticide')
    
    else:
        form = PesticideForm()

    return render(request, 'pesticide/create_pesticide.html', {'form': form})

def edit_pesticide(request, pk):
    pesticide = get_object_or_404(Pesticide, pk=pk)  
    if request.method == "POST":
        form = PesticideForm(request.POST, instance=pesticide)
        if form.is_valid():
            Area = form.cleaned_data.get('Area')
            Year = form.cleaned_data.get('Year')

            if Year and (Year < 1900 or Year > 2100):
                form.add_error('Year', 'L\'année doit être comprise entre 1900 et 2100.')

            # Enregistrer si aucune erreur personnalisée
            if not form.errors:
                form.save()
                return redirect('all_pesticide')
    else:
        form = PesticideForm(instance=pesticide)
    
    return render(request, 'pesticide/edit_pesticide.html', {'form': form})

def delete_pesticide(request, pk):
    pesticide = get_object_or_404(Pesticide, pk=pk)
    if request.method == "POST":
        pesticide.delete()
        return redirect('all_pesticide')
    return render(request, 'pesticide/delete_pesticide.html', {'pesticide': pesticide})

def pesticide_prediction_view(request, pesticide_id=None, predict_all=False):
    # Charger et prétraiter les données
    try:
        data = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/pesticides.csv')
    except FileNotFoundError:
        return HttpResponse("Le fichier CSV des pesticides est introuvable.")

    # Vérifier que le DataFrame n'est pas vide
    if data.empty:
        return HttpResponse("Pas de données disponibles pour la prédiction.")

    # Supprimer les valeurs manquantes
    data.dropna(inplace=True)

    # Nettoyer les noms de colonnes et vérifier la présence des colonnes nécessaires
    data.columns = data.columns.str.strip()  # Nettoie les espaces
    required_columns = ['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Value']
    
    for column in required_columns:
        if column not in data.columns:
            return HttpResponse(f"La colonne '{column}' est manquante dans les données.")

    # Préparer les données pour le modèle
    X = data[required_columns[:-1]]  # Toutes les colonnes sauf 'Value'
    y = data['Value']

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Pipeline pour gérer les colonnes catégorielles et la régression
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

    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Logique de prédiction : prédiction pour un seul pesticide ou pour tous les pesticides
    if predict_all:
        # Prédire pour toutes les lignes du dataset
        predictions = model.predict(X)
        data['Prediction'] = predictions  # Ajouter les prédictions dans le dataset

        page_number = request.GET.get('page', 1)
        paginator = Paginator(data[['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Prediction']].to_dict(orient='records'), 10)
        page_obj = paginator.get_page(page_number)

        context = {
            'all_predictions': page_obj,
            'mse': mean_squared_error(y_test, model.predict(X_test)),
        }

        return render(request, 'pesticide/all_predictions.html', context)

    else:
        # Prédiction pour un pesticide spécifique
        pesticide = get_object_or_404(Pesticide, id=pesticide_id)

        # Créer une entrée de données pour prédire une seule ligne
        new_data = pd.DataFrame([{
            'Domain': pesticide.domain,
            'Area': pesticide.area,
            'Element': pesticide.element,
            'Item': pesticide.item,
            'Year': pesticide.year,
            'Unit': pesticide.unit
        }])

        # Vérifier que les colonnes de new_data correspondent à celles du DataFrame d'origine
        new_data = new_data.reindex(columns=required_columns[:-1], fill_value=0)

        # Faire la prédiction pour l'entrée unique
        prediction = model.predict(new_data)[0]

        # Mettre à jour la valeur dans la base de données
        pesticide.value = prediction
        pesticide.save()  # Enregistrer la prédiction dans l'attribut `value`

        # Préparer le contexte pour afficher la prédiction unique
        context = {
            'prediction': prediction,
            'pesticide': pesticide,
            'mse': mean_squared_error(y_test, model.predict(X_test)),
        }

        return render(request, 'pesticide/prediction_result.html', context)

def store_selected_pesticides(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_pesticides')

        # Vérifier si des pesticides ont été sélectionnés
        if not selected_ids:
            messages.warning(request, 'Aucun pesticide sélectionné.')
            return redirect('all_pesticide')

        # Charger les données existantes dans le fichier CSV
        try:
            pesticide_data = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/pesticides.csv')
        except FileNotFoundError:
            pesticide_data = pd.DataFrame(columns=['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Value'])

        # Récupérer les pesticides correspondants aux IDs sélectionnés
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

        # Enregistrer le DataFrame mis à jour dans le fichier CSV
        pesticide_data.to_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/pesticides.csv', index=False)
        messages.success(request, 'Les données des pesticides sélectionnés ont été ajoutées au fichier CSV avec succès.')
        return redirect('all_pesticide')

    return render(request, 'pesticide/store_selected_pesticides.html')