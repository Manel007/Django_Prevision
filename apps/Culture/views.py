from django.shortcuts import get_object_or_404, redirect, render
from apps.Culture.forms import CultureAgricoleForm
# Create your views here.
from .models import CultureAgricole

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
    if request.method == 'POST':
        form = CultureAgricoleForm(request.POST, instance=culture)
        if form.is_valid():
            form.save()
            return redirect('liste_cultures')  # Rediriger vers la vue qui affiche la liste des cultures
    else:
        form = CultureAgricoleForm(instance=culture)
    return render(request, 'Culture/culture_form.html', {'form': form})

def delete_culture(request, pk):
    culture = get_object_or_404(CultureAgricole, pk=pk)
    
    if request.method == 'POST':
        culture.delete()

    return redirect('liste_cultures')  # Si la méthode n'est pas POST, rediriger directement vers la liste des cultures