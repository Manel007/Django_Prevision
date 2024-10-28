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
            form.save()  # Ne vous inquiétez pas de date_application ici
            return redirect('liste_techniques')
    else:
        form = TechniqueCultureForm()
        form.fields['cultures_associees'].queryset = CultureAgricole.objects.all()

    cultures = CultureAgricole.objects.all()
    return render(request, 'Technique/techniqueculture_form.html', {'form': form, 'cultures': cultures})


def update_technique(request, technique_id):
    technique = get_object_or_404(TechniqueCulture, id=technique_id)
    cultures = CultureAgricole.objects.all()  # Récupérer toutes les cultures

    if request.method == 'POST':
        form = TechniqueCultureForm(request.POST, instance=technique)
        if form.is_valid():
            form.save()
            return redirect('liste_techniques')  # Rediriger vers la liste des techniques ou une autre vue
    else:
        form = TechniqueCultureForm(instance=technique)

    return render(request, 'technique/technique_update.html', {
        'form': form,
        'technique': technique,  # Passer l'objet technique au template
        'cultures': cultures,  # Passer les cultures au template
    })
        
def delete_technique(request, pk):
    technique = get_object_or_404(TechniqueCulture, pk=pk)
    
    if request.method == 'POST':
        technique.delete()

    return redirect('liste_techniques')