from django.shortcuts import render, redirect, get_object_or_404
from .models import Agriculteur
from django.http import HttpResponseRedirect
from django.urls import reverse
import re 
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator



# Create your views here.

def list_agriculteurs(request):
    query = request.GET.get('search', '')  # Récupérer la chaîne de recherche
    agriculteurs = Agriculteur.objects.all()  # Récupérer tous les agriculteurs

    # Si une recherche est effectuée, filtrer les agriculteurs
    if query:
        agriculteurs = agriculteurs.filter(
            Q(nom__icontains=query) | Q(prenom__icontains=query) | Q(contact__icontains=query)
        )
    
    # Ajouter la pagination ici
    paginator = Paginator(agriculteurs, 5)  # Limite à 5 agriculteurs par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'agriculteur/list.html', {
        'page_obj': page_obj,  # Passe l'objet de pagination à votre template
        'search_query': query,  # Passe la chaîne de recherche au template
    })



def create_agriculteurs(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        contact = request.POST.get('contact')
        region = request.POST.get('region')
        adresse = request.POST.get('adresse')

        # Validation des champs
        errors = {
            'nom': None,
            'prenom': None,
            'contact': None,
            'region': None,
            'adresse': None,
        }

        if not nom:
            errors['nom'] = "Le nom est obligatoire."
        
        if not prenom:
            errors['prenom'] = "Le prénom est obligatoire."
        
        if not contact:
            errors['contact'] = "Le contact est obligatoire."
        elif not re.match(r'^\d{8}$', contact):
            errors['contact'] = "Le contact doit contenir exactement 8 chiffres."

        if not region:
            errors['region'] = "La région est obligatoire."

        if not adresse:
            errors['adresse'] = "L'adresse est obligatoire."
        elif len(adresse.split()) < 3:
            errors['adresse'] = "L'adresse doit contenir au moins 3 mots."

        # Si des erreurs existent, renvoyer le formulaire avec les erreurs et les valeurs saisies
        if any(errors.values()):
            return render(request, 'agriculteur/create.html', {
                'errors': errors,
                'nom': nom,
                'prenom': prenom,
                'contact': contact,
                'region': region,
                'adresse': adresse,
            })

        # Créer un nouvel agriculteur
        agriculteur = Agriculteur(
            nom=nom,
            prenom=prenom,
            contact=contact,
            region=region,
            adresse=adresse
        )
        agriculteur.save()
        
        messages.success(request, "Agriculteur créé avec succès.")
        return redirect('list_agriculteurs')

    return render(request, 'agriculteur/create.html')



def delete_agriculteur(request, agriculteur_id):
    agriculteur = get_object_or_404(Agriculteur, id=agriculteur_id)

    if request.method == 'POST':
        agriculteur.delete()
        messages.success(request, "Agriculteur supprimé avec succès.")
        return redirect('list_agriculteurs')

    return render(request, 'agriculteur/list.html')


def edit_agriculteur(request, agriculteur_id):
    agriculteur = get_object_or_404(Agriculteur, id=agriculteur_id)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        contact = request.POST.get('contact')
        region = request.POST.get('region')
        adresse = request.POST.get('adresse')

        # Validation des champs
        errors = {
            'nom': None,
            'prenom': None,
            'contact': None,
            'region': None,
            'adresse': None,
        }

        if not nom:
            errors['nom'] = "Le nom est obligatoire."
        
        if not prenom:
            errors['prenom'] = "Le prénom est obligatoire."
        
        if not contact:
            errors['contact'] = "Le contact est obligatoire."
        elif not re.match(r'^\d{8}$', contact):
            errors['contact'] = "Le contact doit contenir exactement 8 chiffres."

        if not region:
            errors['region'] = "La région est obligatoire."

        if not adresse:
            errors['adresse'] = "L'adresse est obligatoire."
        elif len(adresse.split()) < 3:
            errors['adresse'] = "L'adresse doit contenir au moins 3 mots."

        # Si des erreurs existent, renvoyer le formulaire avec les erreurs et les valeurs saisies
        if any(errors.values()):
            return render(request, 'agriculteur/edit.html', {
                'errors': errors,
                'agriculteur': agriculteur
            })

        # Mettre à jour les données de l'agriculteur
        agriculteur.nom = nom
        agriculteur.prenom = prenom
        agriculteur.contact = contact
        agriculteur.region = region
        agriculteur.adresse = adresse
        agriculteur.save()
        
        messages.success(request, "Agriculteur mis à jour avec succès.")
        return redirect('list_agriculteurs')

    return render(request, 'agriculteur/edit.html', {'agriculteur': agriculteur})