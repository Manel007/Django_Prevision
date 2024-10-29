from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProgrammeDeTraitementForm
from apps.pesticide.models import Pesticide
from .models import ProgrammeDeTraitement
from django.db.models import Q

def all_prog(request):
    search_query = request.GET.get('search', '')
    programmes = ProgrammeDeTraitement.objects.all()

    if search_query:
        
        programmes = programmes.filter(
            Q(nom__icontains=search_query) |
            Q(pesticide__area__icontains=search_query)  
        )

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(programmes, 10)  # 10 programmes par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'programme/all_prog.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

def add_prog(request):
    # Charger tous les pesticides par défaut ou les filtrer selon la zone si besoin
    pesticides = Pesticide.objects.all()

    if request.method == 'POST':
        form = ProgrammeDeTraitementForm(request.POST)
        
        if form.is_valid():
            programme = form.save(commit=False)
            pesticide_id = request.POST.get('pesticide')
            
            if pesticide_id:
                pesticide = get_object_or_404(Pesticide, id=pesticide_id)
                programme.pesticide = pesticide
            
            programme.save()
            return redirect('all_prog')
    else:
        form = ProgrammeDeTraitementForm()

    return render(request, 'programme/add_prog.html', {
        'form': form,
        'pesticides': pesticides,
    })

def delete_prog(request, pk):
    programme = get_object_or_404(ProgrammeDeTraitement, pk=pk)
    if request.method == "POST":
        programme.delete()
        return redirect('all_prog')
    return render(request, 'programme/delete_prog.html', {'programme': programme}) 


def edit_prog(request, pk):
    # Récupérer le programme à modifier
    programme = get_object_or_404(ProgrammeDeTraitement, pk=pk)
    pesticides = Pesticide.objects.all()

    if request.method == 'POST':
        # Mettre à jour le programme avec les données du formulaire
        programme.nom = request.POST.get('nom')
        programme.description = request.POST.get('description')
        pesticide_id = request.POST.get('pesticide')

        if pesticide_id:
            pesticide = get_object_or_404(Pesticide, id=pesticide_id)
            programme.pesticide = pesticide
        
        programme.frequence_application = request.POST.get('frequence_application')
        programme.save()
        
        return redirect('all_prog')

    return render(request, 'programme/edit_prog.html', {
        'programme': programme,
        'pesticides': pesticides,
    })

def details_prog(request, pk):
    programme = get_object_or_404(ProgrammeDeTraitement, pk=pk)
    return render(request, 'programme/details_prog.html', {
        'programme': programme
    })


def front_prog(request):
    programmes = ProgrammeDeTraitement.objects.all()  
    return render(request, 'programme/front_prog.html', {'programmes': programmes})