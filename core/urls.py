# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include 
from apps.Culture import views
from apps.Technique import views as technique_views
from apps.RecommendationTech import views as recommend_views


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
    path('cultures/', views.liste_cultures, name='liste_cultures'),
    path('createCulture/', views.create_culture, name='create_culture'),
    path('updateCulture/<int:pk>/', views.update_culture, name='update_culture'),
    path('deleteCulture/<int:pk>/', views.delete_culture, name='delete_culture'),
   path('techniques/', technique_views.liste_techniques, name='liste_techniques'),
    path('createTechnique/', technique_views.create_technique, name='create_technique'),
    path('updateTechnique<int:technique_id>/', technique_views.update_technique, name='update_technique'),
    path('deleteTechnique/<int:pk>/', technique_views.delete_technique, name='delete_technique'),
    path('recommander/', recommend_views.recommend_view, name='recommend_view'),
    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),

]
