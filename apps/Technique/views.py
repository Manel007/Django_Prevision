
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from apps.Culture.models import CultureAgricole
from .models import TechniqueCulture
from .forms import TechniqueCultureForm

def liste_techniques(request):
    techniques = TechniqueCulture.objects.all()
    return render(request, 'Technique/techniqueculture_list.html', {'techniques': techniques})

def nouvelle_liste_techniques(request):
    techniques = TechniqueCulture.objects.all()  
    paginator = Paginator(techniques, 4)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'Technique/techniques_front.html', {'page_obj': page_obj})

def technique_details(request, pk):
    technique = get_object_or_404(TechniqueCulture, pk=pk)
    return render(request, 'Technique/technique_detailsBack.html', {'technique': technique})

def detail_technique(request, technique_id):
    technique = get_object_or_404(TechniqueCulture, id=technique_id)
    return render(request, 'Technique/technique_detail.html', {'technique': technique})

def create_technique(request):
    if request.method == 'POST':
        form = TechniqueCultureForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('liste_techniques')
    else:
        form = TechniqueCultureForm()
        form.fields['cultures_associees'].queryset = CultureAgricole.objects.all()

    cultures = CultureAgricole.objects.all()
    return render(request, 'Technique/techniqueculture_form.html', {'form': form, 'cultures': cultures})


def update_technique(request, technique_id):
    technique = get_object_or_404(TechniqueCulture, id=technique_id)
    cultures = CultureAgricole.objects.all()  

    if request.method == 'POST':
        form = TechniqueCultureForm(request.POST, instance=technique)
        if form.is_valid():
            form.save()
            return redirect('liste_techniques')  
    else:
        form = TechniqueCultureForm(instance=technique)

    return render(request, 'technique/technique_update.html', {
        'form': form,
        'technique': technique,  
        'cultures': cultures,  
    })
        
def delete_technique(request, pk):
    technique = get_object_or_404(TechniqueCulture, pk=pk)
    
    if request.method == 'POST':
        technique.delete()

    return redirect('liste_techniques')