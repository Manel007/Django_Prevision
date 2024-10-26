# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from apps.Culture import views

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    
    # ADD NEW Routes HERE
    path('cultures/', views.liste_cultures, name='liste_cultures'),
    path('create/', views.create_culture, name='create_culture'),
    path('update/<int:pk>/', views.update_culture, name='update_culture'),
    path('delete/<int:pk>/', views.delete_culture, name='delete_culture'),
    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls"))
]
