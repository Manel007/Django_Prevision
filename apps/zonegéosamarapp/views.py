

from .models import ZoneGeographique
from .forms import *
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

def ZoneList(request):
    zones = ZoneGeographique.objects.all()

    query = request.GET.get('search', '')
    zones = ZoneGeographique.objects.filter(nomZone__icontains=query)  
    paginator = Paginator(zones, 8) 
    page_number = request.GET.get('page')
    zones = paginator.get_page(page_number)

   

    context = {
        'zones': zones,
        'search_query': query,
    }


    return render(request, 'zones/zone_list.html', context)

def ZoneCreate(request):
    if request.method == 'POST':
        form = ZoneGeographiqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zone_list') 
    else:
        form = ZoneGeographiqueForm()
    return render(request, 'zones/zone_form.html', {'form': form})

def ZoneUpdate(request, pk):
    zone = get_object_or_404(ZoneGeographique, pk=pk)
    if request.method == 'POST':
        form = ZoneGeographiqueForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return redirect('zone_list') 
    else:
        form = ZoneGeographiqueForm(instance=zone)
    return render(request, 'zones/zone_form.html', {'form': form})

def ZoneDelete(request, pk):
    zone = get_object_or_404(ZoneGeographique, pk=pk)
    if request.method == 'POST':
        zone.delete()
    return redirect('zone_list')  




def TypeSolList(request):
    query = request.GET.get('search', '')
    types_sol = TypeDeSol.objects.filter(nomTypeSol__icontains=query)
    paginator = Paginator(types_sol, 8)  

    page_number = request.GET.get('page')
    types_sol = paginator.get_page(page_number)

    context = {
        'types_sol': types_sol,
        'search_query': query,  
    }
    return render(request, 'typesol/typesol_list.html', context)

def TypeSolCreate(request):
    if request.method == 'POST':
        form = TypeDeSolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('typesol_list')  
    else:
        form = TypeDeSolForm()
    return render(request, 'typesol/typesol_form.html', {'form': form})

def TypeSolUpdate(request, pk):
    type_sol = get_object_or_404(TypeDeSol, pk=pk)
    if request.method == 'POST':
        form = TypeDeSolForm(request.POST, instance=type_sol)
        if form.is_valid():
            form.save()
            return redirect('typesol_list') 
    else:
        form = TypeDeSolForm(instance=type_sol)
    return render(request, 'typesol/typesol_form.html', {'form': form})

def TypeSolDelete(request, pk):
    type_sol = get_object_or_404(TypeDeSol, pk=pk)
    if request.method == 'POST':
        type_sol.delete()
        return redirect('typesol_list')  
    return render(request, 'typesol/type_sol_confirm_delete.html', {'type_sol': type_sol})  