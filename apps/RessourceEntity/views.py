from django.shortcuts import render, redirect, get_object_or_404
from .models import Ressource ,Fournisseur
from .forms import RessourceForm ,FournisseurForm 
from django.db.models import Q

import pandas as pd
from .forms import PredictForm
from sklearn.ensemble import RandomForestRegressor

# Charger le modèle pré-entrainé et les données une seule fois
data = pd.read_csv('apps/RessourceEntity/Ressourceee.csv')  # Adapter le chemin
X = pd.get_dummies(data[['nom_ressource', 'Saison']], drop_first=True)
y = data['quantite']

# Entraîner le modèle une seule fois
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

def predict_view(request):
    predicted_quantity = None  # Initialiser la variable

    if request.method == 'POST':
        form = PredictForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            nom_ressource = form.cleaned_data['nom_ressource']
            saison = form.cleaned_data['saison']

            # Créer une nouvelle donnée pour la prédiction
            new_data = pd.get_dummies(pd.DataFrame(
                [[nom_ressource, saison]], columns=['nom_ressource', 'Saison']
            ), drop_first=True)

            # S'assurer que les colonnes correspondent à l'entraînement
            new_data = new_data.reindex(columns=X.columns, fill_value=0)

            # Faire la prédiction
            predicted_quantity = model.predict(new_data)[0]

    else:
        form = PredictForm()

    return render(request, 'PredictRessourceQuantity/predictressource.html', {
        'form': form, 'predicted_quantity': predicted_quantity
    })





# Liste des ressources
def ressource_list(request):
    ressources = Ressource.objects.all()
    return render(request, 'ressource/ressource_list.html', {'ressources': ressources})

# Détail d'une ressource
def ressource_detail(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    return render(request, 'ressource/detail_ressource.html', {'ressource': ressource})

# Création d'une nouvelle ressource
def ressource_create(request):
    if request.method == "POST":
        form = RessourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ressource_list')  # Redirige vers la liste des ressources
    else:
        form = RessourceForm()
    return render(request, 'ressource/ressource_form.html', {'form': form})

# Modification d'une ressource
def ressource_update(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    if request.method == "POST":
        form = RessourceForm(request.POST, instance=ressource)
        if form.is_valid():
            form.save()
            return redirect('ressource_list')  # Redirige vers la liste
    else:
        form = RessourceForm(instance=ressource)
    return render(request, 'ressource/ressource_form.html', {'form': form})

# Suppression d'une ressource
def ressource_delete(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    if request.method == "POST":
        ressource.delete()
        return redirect('ressource_list')  # Redirige vers la liste après suppression
    return render(request, 'ressource/ressource_confirm_delete.html', {'ressource': ressource})

# Recherche de ressource par attribut
def ressource_search(request):
    query = request.GET.get('q', '')
    attribute = request.GET.get('attribute', '')

    # Dictionnaire pour mapper les attributs à leurs noms dans le modèle
    attribute_map = {
        'type_ressource': 'type_ressource__icontains',
        'zone': 'zone__icontains',
        'unite_mesure': 'unite_mesure__icontains',
    }

    if attribute in attribute_map:
        filter_condition = {attribute_map[attribute]: query}
        results = Ressource.objects.filter(**filter_condition)
    else:
        results = Ressource.objects.all()  # Si aucun attribut valide n'est sélectionné

    return render(request, 'ressource/ressource_list.html', {'ressources': results, 'query': query})








# Liste des fournisseurs
def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseur/fournisseur_list.html', {'fournisseurs': fournisseurs})

# Détail d'un fournisseur
def fournisseur_detail(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    return render(request, 'fournisseur/detail_fournisseur.html', {'fournisseur': fournisseur})



# Création d'un nouveau fournisseur
def fournisseur_create(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fournisseur_list')  # Redirige vers la liste des fournisseurs
    else:
        form = FournisseurForm()

    return render(request, 'Fournisseur/fournisseur_form.html', {'form': form})

# Modification d'un fournisseur
def fournisseur_update(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == "POST":
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect('fournisseur_list')  # Redirige vers la liste
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'Fournisseur/fournisseur_form.html', {'form': form})

# Suppression d'un fournisseur
def fournisseur_delete(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == "POST":
        fournisseur.delete()
        return redirect('fournisseur_list')  # Redirige vers la liste après suppression
    return render(request, 'Fournisseur/fournisseur_confirm_delete.html', {'fournisseur': fournisseur})

