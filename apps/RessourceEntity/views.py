from django.shortcuts import render, redirect, get_object_or_404
from .models import Ressource
from .forms import RessourceForm
from django.db.models import Q

# Liste des ressources
def ressource_list(request):
    ressources = Ressource.objects.all()
    return render(request, 'ressource/liste_ressources.html', {'ressources': ressources})

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
    results = Ressource.objects.filter(
        Q(type_ressource__icontains=query) |
        Q(zone__icontains=query) |
        Q(unite_mesure__icontains=query)
    )
    return render(request, 'ressource/liste_ressources.html', {'ressources': results, 'query': query})
