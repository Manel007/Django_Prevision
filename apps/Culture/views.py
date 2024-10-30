from django.shortcuts import get_object_or_404, redirect, render
from apps.Culture.forms import CultureAgricoleForm
from apps.Technique.models import TechniqueCulture
from .models import CultureAgricole
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from apps.Culture import models
from django.db.models import Q
from sklearn.neighbors import KNeighborsClassifier
from django.core.paginator import Paginator


def liste_cultures(request):
    cultures = CultureAgricole.objects.all()
    return render(request, 'Culture/liste_cultures.html', {'cultures': cultures})

def culture_list(request):
    culture_list = CultureAgricole.objects.all()
    paginator = Paginator(culture_list, 4)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    return render(request, 'Culture/cultures_front.html', {'page_obj': page_obj})


def culture_detail(request, pk):
    culture = get_object_or_404(CultureAgricole, pk=pk)
    return render(request, 'Culture/culture_detail.html', {'culture': culture})

def culture_details(request, pk):
    culture = get_object_or_404(CultureAgricole, pk=pk)
    return render(request, 'Culture/culture_detailsBack.html', {'culture': culture})

def create_culture(request):
    if request.method == 'POST':
        form = CultureAgricoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_cultures')  
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



