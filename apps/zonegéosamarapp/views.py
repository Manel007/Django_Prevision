

from .models import ZoneGeographique
from .forms import *
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
import importlib
from django.http import JsonResponse

from .anomaly_detection import detect_anomalies
@login_required(login_url="/login/")

def TypesolDisplayFront(request):
    query = request.GET.get('search', '')
    types_sol = TypeDeSol.objects.filter(nomTypeSol__icontains=query)
    paginator = Paginator(types_sol, 6)  

    page_number = request.GET.get('page')
    types_sol = paginator.get_page(page_number)

    context = {
        'types_sol': types_sol,
        'search_query': query,  
    }
    return render(request, 'front/zones+typesol/display-typesol.html', context)
@login_required(login_url="/login/")

def ZoneDisplayFront(request):
    zones = ZoneGeographique.objects.all()

    query = request.GET.get('search', '')
    zones = ZoneGeographique.objects.filter(nomZone__icontains=query)  
    paginator = Paginator(zones, 6) 
    page_number = request.GET.get('page')
    zones = paginator.get_page(page_number)

    context = {
        'zones': zones,
        'search_query': query,
    }

    return render(request, 'front/zones+typesol/display-zones.html', context)
@login_required(login_url="/login/")

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
@login_required(login_url="/login/")

def ZoneCreate(request):
    if request.method == 'POST':
        form = ZoneGeographiqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zone_list') 
    else:
        form = ZoneGeographiqueForm()
    return render(request, 'zones/zone_form.html', {'form': form})
@login_required(login_url="/login/")

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
@login_required(login_url="/login/")

def ZoneDelete(request, pk):
    zone = get_object_or_404(ZoneGeographique, pk=pk)
    if request.method == 'POST':
        zone.delete()
    return redirect('zone_list')  



@login_required(login_url="/login/")

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
@login_required(login_url="/login/")

def TypeSolCreate(request):
    if request.method == 'POST':
        form = TypeDeSolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('typesol_list')  
    else:
        form = TypeDeSolForm()
    return render(request, 'typesol/typesol_form.html', {'form': form})
@login_required(login_url="/login/")

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
@login_required(login_url="/login/")

def TypeSolDelete(request, pk):
    type_sol = get_object_or_404(TypeDeSol, pk=pk)
    if request.method == 'POST':
        type_sol.delete()
        return redirect('typesol_list')  
    return render(request, 'typesol/type_sol_confirm_delete.html', {'type_sol': type_sol})  

from django.http import JsonResponse
from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
@login_required(login_url="/login/")

# Partie AI
@csrf_exempt
def dataset_anomalies_view(request):
    if request.method == 'POST':
   
        anomalies_data = detect_anomalies() 
        return JsonResponse({
            'anomalies': anomalies_data['anomalies'],
            'count': anomalies_data['count']
        })

    return render(request, 'typesol/dataset_anomalies.html')


    

predict_soil_module = importlib.import_module('apps.zonegéosamarapp.AI soil type prediction.predict_soil')
predict_soil_type = predict_soil_module.predict_soil_type
@login_required(login_url="/login/")

def predict_soil(request):
    if request.method == 'POST':
        try:
            
            pH_level = float(request.POST.get('pH_level'))
            organic_matter = float(request.POST.get('organic_matter'))
            nitrogen_content = float(request.POST.get('nitrogen_content'))
            phosphorus_content = float(request.POST.get('phosphorus_content'))
            potassium_content = float(request.POST.get('potassium_content'))

           
            soil_type = predict_soil_type(pH_level, organic_matter, nitrogen_content, phosphorus_content, potassium_content)

            
            return JsonResponse({'predicted_soil_type': soil_type})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'front/zones+typesol/predict-soil.html')
@login_required(login_url="/login/")

def soil_prediction_form(request):
    return render(request, 'front/zones+typesol/predict-soil.html')   