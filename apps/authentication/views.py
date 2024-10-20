# apps/authentication/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from .models import Culture  # Adjust import according to your model's location
from django.http import JsonResponse
from .forms import CultureForm  # Assuming you have a form for Culture
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # Uncomment the following line if you want to redirect to the login page after registration
            # return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def culture_list(request):
    cultures = Culture.objects.all()
    return render(request, 'home/culture_list.html', {'cultures': cultures})

def culture_create(request):
    if request.method == "POST":
        # Retrieve form data
        nom = request.POST.get('nom')
        type_culture = request.POST.get('type_culture')
        duree_croissance = request.POST.get('duree_croissance')
        superficie_requise = request.POST.get('superficie_requise')
        conditions_optimales = request.POST.get('conditions_optimales')

        # Create a new culture if all fields are provided
        if all([nom, type_culture, duree_croissance, superficie_requise, conditions_optimales]):
            Culture.objects.create(
                nom=nom,
                type_culture=type_culture,
                duree_croissance=duree_croissance,
                superficie_requise=superficie_requise,
                conditions_optimales=conditions_optimales
            )
            return redirect('culture_list')  # Redirect to the culture list after creation
        else:
            msg = "Please fill in all fields."  # Error message for incomplete form
        
    return render(request, 'home/culture_form.html')  # Render the form
def culture_update(request, culture_id):  # Use 'culture_id' here
    culture = get_object_or_404(Culture, id=culture_id)

    if request.method == 'POST':
        culture.nom = request.POST.get('nom')
        culture.type_culture = request.POST.get('type_culture')
        culture.duree_croissance = request.POST.get('duree_croissance')
        culture.superficie_requise = request.POST.get('superficie_requise')
        culture.conditions_optimales = request.POST.get('conditions_optimales')
        culture.save()
        return redirect('culture_list')

    return render(request, 'home/culture_form.html', {'culture': culture})


def culture_delete(request, culture_id):
    culture = get_object_or_404(Culture, id=culture_id)
    print("Attempting to delete culture:", culture.nom)

    if request.method == 'POST':
        culture.delete()
        print("Culture deleted.")
        return JsonResponse({'success': True})

    return render(request, 'home/culture_confirm_delete.html', {'culture': culture})