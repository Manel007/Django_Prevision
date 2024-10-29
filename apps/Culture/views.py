from django.shortcuts import get_object_or_404, redirect, render
from apps.Culture.forms import CultureAgricoleForm
from apps.Technique.models import TechniqueCulture
# Create your views here.
from .models import CultureAgricole
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from apps.Culture import models
from django.db.models import Q
from sklearn.neighbors import KNeighborsClassifier


def liste_cultures(request):
    cultures = CultureAgricole.objects.all()
    return render(request, 'Culture/liste_cultures.html', {'cultures': cultures})

def create_culture(request):
    if request.method == 'POST':
        form = CultureAgricoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_cultures')  # Rediriger vers la vue qui affiche la liste des cultures
    else:
        form = CultureAgricoleForm()
    return render(request, 'Culture/culture_form.html', {'form': form})

def update_culture(request, pk):
    culture = get_object_or_404(CultureAgricole, pk=pk)
    form = CultureAgricoleForm(instance=culture)
    
    if request.method == 'POST':
        form = CultureAgricoleForm(request.POST, instance=culture)
        if form.is_valid():
            form.save()
            return redirect('liste_cultures')  

    context = {'form': form, 'culture': culture}
    return render(request, 'Culture/culture_update.html', context)

def delete_culture(request, pk):
    culture = get_object_or_404(CultureAgricole, pk=pk)
    
    if request.method == 'POST':
        culture.delete()

    return redirect('liste_cultures')  



