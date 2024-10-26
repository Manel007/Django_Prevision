# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.urls import path
from apps.zonegéosamarapp import views


urlpatterns = [
    
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE

 

path('zones/', views.ZoneList, name='zone_list'),  # Liste des zones
path('zones/create', views.ZoneCreate, name='zone_form'),  # créer une nouvelle zone géo
path('zones/update/<int:pk>/', views.ZoneUpdate, name='zone_update'),  # créer une nouvelle zone géo
 path('zones/delete/<int:pk>/', views.ZoneDelete, name='zone_delete'),

# Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),
    
]
