from django.shortcuts import render, redirect, get_object_or_404
from .models import Agriculteur
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def list_agriculteurs(request):
    agriculteurs = Agriculteur.objects.all()  # Récupérer tous les agriculteurs
    return render(request, 'agriculteur/list.html', {
        'agriculteurs': agriculteurs,
    })


def create_agriculteurs(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        contact = request.POST.get('contact')
        adresse = request.POST.get('adresse')
        region = request.POST.get('region')

        # Créer un nouvel agriculteur et sauvegarder dans la base de données
        Agriculteur.objects.create(nom=nom, prenom=prenom, contact=contact, adresse=adresse, region=region)

        return redirect('list_agriculteurs')  # Rediriger vers la liste après création

    return render(request, 'agriculteur/create.html')  # Afficher le formulaire vide     


def delete_agriculteur(request, agriculteur_id):
    agriculteur = get_object_or_404(Agriculteur, id=agriculteur_id)

    if request.method == 'POST':
        agriculteur.delete()
        return redirect('list_agriculteurs')

    return render(request, 'agriculteur/list.html')


def edit_agriculteur(request, agriculteur_id):
    agriculteur = get_object_or_404(Agriculteur, id=agriculteur_id)

    if request.method == "POST":
        agriculteur.nom = request.POST.get('nom')
        agriculteur.prenom = request.POST.get('prenom')
        agriculteur.contact = request.POST.get('contact')
        agriculteur.adresse = request.POST.get('adresse')
        agriculteur.region = request.POST.get('region')
        agriculteur.save()
        return redirect('list_agriculteurs')  

    return render(request, 'agriculteur/edit.html', {'agriculteur': agriculteur})