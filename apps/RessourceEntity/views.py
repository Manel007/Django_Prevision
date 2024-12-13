from django.shortcuts import render, redirect, get_object_or_404
from .models import Ressource ,Fournisseur
from .forms import RessourceForm ,FournisseurForm 
from django.db.models import Q

import pandas as pd
from .forms import PredictForm
from sklearn.ensemble import RandomForestRegressor
from .forms import PredictForm
import logging
# Configurer le logger
logger = logging.getLogger(__name__)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Charger et préparer les données une seule fois
data = pd.read_csv('apps/RessourceEntity/Ressourcee.csv')  # Vérifiez le chemin
X = pd.get_dummies(data[['nom_ressource', 'Saison']], drop_first=True)
y = data['quantite']

# Entraîner le modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Stocker les colonnes utilisées pour l'entraînement
training_columns = X.columns
@login_required(login_url="/login/")

def predict_view(request):
    predicted_quantity = None  # Initialisation par défaut

    if request.method == 'POST':
        form = PredictForm(request.POST)
        if form.is_valid():
            # Extraire les données du formulaire
            nom_ressource = form.cleaned_data['nom_ressource']  # Récupérer directement la valeur
            Saison = form.cleaned_data['Saison']

            # Journaliser les valeurs saisies
            logger.info(f"Form data - nom_ressource: {nom_ressource}, Saison: {Saison}")

            # Préparer les données pour la prédiction
            new_data = pd.DataFrame(
                [[nom_ressource, Saison]], columns=['nom_ressource', 'Saison']
            )

            # Log des nouvelles données
            logger.info(f"Nouvelles données avant transformation: {new_data}")

            # Encodez les nouvelles données
            new_data = pd.get_dummies(new_data, drop_first=True)

            # Réindexez pour correspondre aux colonnes d'entraînement
            new_data = new_data.reindex(columns=training_columns, fill_value=0)

            # Log des données préparées
            logger.info(f"Données préparées pour la prédiction: {new_data}")

            # Prédire la quantité et journaliser le résultat
            predicted_quantity = model.predict(new_data)[0]
            logger.info(f"Quantité prédite: {predicted_quantity}")
        else:
            logger.error("Formulaire non valide")
    else:
        form = PredictForm()

    return render(request, 'PredictRessourceQuantity/predictressource.html', {
        'form': form, 'predicted_quantity': predicted_quantity
    })

@login_required(login_url="/login/")



# Liste des ressources
def ressource_list(request):
    ressources = Ressource.objects.all()
    return render(request, 'ressource/ressource_list.html', {'ressources': ressources})
@login_required(login_url="/login/")


def ressource_listFront(request):
    # Fetch all ressources and order them (e.g., by name)
    ressources = Ressource.objects.all().order_by('nom_ressource')  # Change 'nom_ressource' to the desired field for ordering

    paginator = Paginator(ressources, 10)  # Paginate the ordered resources
    page_number = request.GET.get('page')
    all_ressources = paginator.get_page(page_number)

    return render(request, 'ressource/ressource_listFront.html', {'all_ressources': all_ressources})
@login_required(login_url="/login/")


# Détail d'une ressource
def ressource_detail(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    return render(request, 'ressource/detail_ressource.html', {'ressource': ressource})
@login_required(login_url="/login/")

def ressource_create(request):
    if request.method == "POST":
        form = RessourceForm(request.POST)
        if form.is_valid():
            ressource = form.save()  # Enregistre la ressource
            return redirect('ressource_list')  # Redirige vers la liste des ressources
    else:
        form = RessourceForm()

    return render(request, 'ressource/ressource_form.html', {'form': form})
@login_required(login_url="/login/")

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
@login_required(login_url="/login/")

# Suppression d'une ressource
def ressource_delete(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    if request.method == "POST":
        ressource.delete()
        return redirect('ressource_list')  # Redirige vers la liste après suppression
    return render(request, 'ressource/ressource_confirm_delete.html', {'ressource': ressource})
@login_required(login_url="/login/")

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



@login_required(login_url="/login/")





# Liste des fournisseurs
def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseur/fournisseur_list.html', {'fournisseurs': fournisseurs})
@login_required(login_url="/login/")


def fournisseur_listFront(request):
    # Récupérer tous les fournisseurs et les ordonner (par exemple par nom)
    fournisseurs = Fournisseur.objects.all().order_by('nom')  # Change 'nom' to the desired field for ordering

    # Implémenter la recherche
    search_query = request.GET.get('search', '')
    if search_query:
        fournisseurs = fournisseurs.filter(nom__icontains=search_query)

    paginator = Paginator(fournisseurs, 10)  # Pagination des fournisseurs ordonnés
    page_number = request.GET.get('page')
    all_fournisseurs = paginator.get_page(page_number)

    return render(request, 'Fournisseur/fournisseur_listFront.html', {
        'all_fournisseurs': all_fournisseurs,
        'search_query': search_query,
    })
@login_required(login_url="/login/")

# Détail d'un fournisseur
def fournisseur_detail(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    return render(request, 'fournisseur/detail_fournisseur.html', {'fournisseur': fournisseur})
@login_required(login_url="/login/")


def fournisseur_create(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST)
        if form.is_valid():
            fournisseur = form.save(commit=False)
            # Traiter les ressources fournies
            # Vous pouvez les stocker comme une chaîne ou les traiter selon vos besoins.
            fournisseur.save()
            return redirect('fournisseur_list')  # Redirige vers la liste des fournisseurs
    else:
        form = FournisseurForm()

    return render(request, 'Fournisseur/fournisseur_form.html', {'form': form})
# Modification d'un fournisseur
@login_required(login_url="/login/")

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
@login_required(login_url="/login/")

# Suppression d'un fournisseur
def fournisseur_delete(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == "POST":
        fournisseur.delete()
        return redirect('fournisseur_list')  # Redirige vers la liste après suppression
    return render(request, 'Fournisseur/fournisseur_confirm_delete.html', {'fournisseur': fournisseur})

