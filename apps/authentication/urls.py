

from django.urls import path
from .views import login_view, register_user 
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),  
    path("logout/", LogoutView.as_view(), name="logout"), 


## views.py
#from django.contrib.auth import logout
#from django.shortcuts import redirect

#def logout_view(request):
 #   logout(request)
 #   return redirect('login')  # Redirige vers la page de connexion après la déconnexion












]
