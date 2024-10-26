

from .models import ZoneGeographique
from .forms import *
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render

def ZoneList(request):
    zones = ZoneGeographique.objects.all()
    return render(request, 'zones/zone_list.html', {'zones': zones})

def ZoneCreate(request):
    if request.method == 'POST':
        form = ZoneGeographiqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zone_list')  # Rediriger vers la vue qui affiche la liste des zones
    else:
        form = ZoneGeographiqueForm()
    return render(request, 'zones/zone_form.html', {'form': form})

def ZoneUpdate(request, pk):
    zone = get_object_or_404(ZoneGeographique, pk=pk)
    if request.method == 'POST':
        form = ZoneGeographiqueForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return redirect('zone_list')  # Rediriger vers la vue qui affiche la liste des zones
    else:
        form = ZoneGeographiqueForm(instance=zone)
    return render(request, 'zones/zone_form.html', {'form': form})

def ZoneDelete(request, pk):
    zone = get_object_or_404(ZoneGeographique, pk=pk)
    if request.method == 'POST':
        zone.delete()
    return redirect('zone_list')  




def TypeSolList(request):
    types_sol = TypeDeSol.objects.all()
    return render(request, 'typesol/typesol_list.html', {'types_sol': types_sol})

def TypeSolCreate(request):
    if request.method == 'POST':
        form = TypeDeSolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('typesol_list')  # Redirect to the view that displays the list of soil types
    else:
        form = TypeDeSolForm()
    return render(request, 'typesol/typesol_form.html', {'form': form})

def TypeSolUpdate(request, pk):
    type_sol = get_object_or_404(TypeDeSol, pk=pk)
    if request.method == 'POST':
        form = TypeDeSolForm(request.POST, instance=type_sol)
        if form.is_valid():
            form.save()
            return redirect('typesol_list')  # Redirect to the view that displays the list of soil types
    else:
        form = TypeDeSolForm(instance=type_sol)
    return render(request, 'typesol/typesol_form.html', {'form': form})

def TypeSolDelete(request, pk):
    type_sol = get_object_or_404(TypeDeSol, pk=pk)
    if request.method == 'POST':
        type_sol.delete()
        return redirect('type_sol_list')  # Redirect to the view that displays the list of soil types
    return render(request, 'typesol/type_sol_confirm_delete.html', {'type_sol': type_sol})  