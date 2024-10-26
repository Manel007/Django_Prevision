# Importations nécessaires
from django.shortcuts import get_object_or_404, redirect, render

from apps.Culture.models import CultureAgricole
from .models import TechniqueCulture
from .forms import TechniqueCultureForm

def liste_techniques(request):
    techniques = TechniqueCulture.objects.all()
    return render(request, 'Technique/techniqueculture_list.html', {'techniques': techniques})

def create_technique(request):
    if request.method == 'POST':
        form = TechniqueCultureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_techniques')
    else:
        form = TechniqueCultureForm()
        form.fields['cultures_associees'].queryset = CultureAgricole.objects.all()  # Passer les cultures existantes au formulaire

    cultures = CultureAgricole.objects.all()  # Récupérer toutes les cultures pour affichage dans le formulaire

    return render(request, 'Technique/techniqueculture_form.html', {'form': form, 'cultures': cultures})

def update_technique(request, pk):
    technique = get_object_or_404(TechniqueCulture, pk=pk)
    form = TechniqueCultureForm(instance=technique)
    
    if request.method == 'POST':
        form = TechniqueCultureForm(request.POST, instance=technique)
        if form.is_valid():
            form.save()
            return redirect('liste_techniques')  

    context = {'form': form, 'technique': technique}
    return render(request, 'Technique/technique_update.html', context)

def delete_technique(request, pk):
    technique = get_object_or_404(TechniqueCulture, pk=pk)
    
    if request.method == 'POST':
        technique.delete()

    return redirect('liste_techniques')