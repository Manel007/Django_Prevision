# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from apps.RessourceEntity import views
urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("agriculteurs/", include('apps.agriculteur.urls')),  
    path("generateimage/", include('apps.images.urls')),  
    path("rocVocal/", include('apps.reconnaissancevoc.urls')), 
    path("", include('apps.pesticide.urls')), 
    path("programme_trait/", include('apps.programme.urls')),  
    path("", include('apps.front.urls')),  
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include('apps.agriculture_project.agriculture_project.urls')),
    path("", include('apps.front.urls')),  

    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
 

  path('ressource_list/', views.ressource_list, name='ressource_list'),
    path('ressource/<int:pk>/', views.ressource_detail, name='ressource_detail'),
    path('ressource/new/', views.ressource_create, name='ressource_create'),
    path('ressource/<int:pk>/edit/', views.ressource_update, name='ressource_update'),
    path('ressource/<int:pk>/delete/', views.ressource_delete, name='ressource_delete'),
    path('search/', views.ressource_search, name='ressource_search'),

    path('fournisseurs/', views.fournisseur_list, name='fournisseur_list'),
    path('fournisseurs/<int:pk>/', views.fournisseur_detail, name='fournisseur_detail'),
    path('fournisseurs/new/', views.fournisseur_create, name='fournisseur_create'),
    path('fournisseurs/<int:pk>/edit/', views.fournisseur_update, name='fournisseur_update'),
    path('fournisseurs/<int:pk>/delete/', views.fournisseur_delete, name='fournisseur_delete'),
     path('predict/', views.predict_view, name='predict'),

  path("", include("apps.home.urls"))

]
