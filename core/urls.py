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

path('typesol/', views.TypeSolList ,name='typesol_list'),
path('typesol/create/', views.TypeSolCreate, name='typesol_form'),
path('typesol/update/<int:pk>/', views.TypeSolUpdate, name='type_sol_update'),
path('typesol/delete/<int:pk>/', views.TypeSolDelete, name='type_sol_delete'),




path('dataset-anomalies/', views.dataset_anomalies_view, name='dataset_anomalies'),

path('predict-soil/', views.predict_soil, name='predict_soil'),
path('soil-prediction-form/', views.soil_prediction_form, name='soil_prediction_form'),  # Ensure this path exists
# Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),
    
]
