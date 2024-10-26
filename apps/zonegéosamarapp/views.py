

from .models import ZoneGeographique
from .forms import ZoneGeographiqueForm
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