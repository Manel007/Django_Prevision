from django.shortcuts import render, redirect, get_object_or_404
from .models import Ressource
from .forms import RessourceForm
from django.db.models import Q

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