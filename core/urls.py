

from django.contrib import admin
from django.urls import path, include 
from apps.Culture import views
from apps.Technique import views as technique_views
from apps.RecommendationTech import views as recommend_views
from django.urls import path, include 
from django.urls import path
from apps.zonegéosamarapp import views as viewszone


from apps.RessourceEntity import views as ressourceview
urlpatterns = [
    
    path('admin/', admin.site.urls),          
    path("agriculteurs/", include('apps.agriculteur.urls')),  
    path("generateimage/", include('apps.images.urls')),  
    path("rocVocal/", include('apps.reconnaissancevoc.urls')), 
    path("", include('apps.pesticide.urls')), 
    path("programme_trait/", include('apps.programme.urls')),  
    path("", include('apps.front.urls')),  
    path("", include("apps.authentication.urls")),
    path("", include('apps.agriculture_project.agriculture_project.urls')),
    path("", include('apps.front.urls')),  

    path('cultures/', views.liste_cultures, name='liste_cultures'),
    path('createCulture/', views.create_culture, name='create_culture'),
    path('updateCulture/<int:pk>/', views.update_culture, name='update_culture'),
    path('deleteCulture/<int:pk>/', views.delete_culture, name='delete_culture'),
   path('techniques/', technique_views.liste_techniques, name='liste_techniques'),
    path('createTechnique/', technique_views.create_technique, name='create_technique'),
    path('updateTechnique<int:technique_id>/', technique_views.update_technique, name='update_technique'),
    path('deleteTechnique/<int:pk>/', technique_views.delete_technique, name='delete_technique'),
    path('recommander/', recommend_views.recommend_view, name='recommend_view'),
   



 

path('zones/', viewszone.ZoneList, name='zone_list'), 
path('zones/create', viewszone.ZoneCreate, name='zone_form'),  
path('zones/update/<int:pk>/', viewszone.ZoneUpdate, name='zone_update'),
path('zones/delete/<int:pk>/', viewszone.ZoneDelete, name='zone_delete'),

path('typesol/', viewszone.TypeSolList ,name='typesol_list'),
path('typesol/create/', viewszone.TypeSolCreate, name='typesol_form'),
path('typesol/update/<int:pk>/', viewszone.TypeSolUpdate, name='type_sol_update'),
path('typesol/delete/<int:pk>/', viewszone.TypeSolDelete, name='type_sol_delete'),




path('dataset-anomalies/', viewszone.dataset_anomalies_view, name='dataset_anomalies'),

path('predict-soil/', viewszone.predict_soil, name='predict_soil'),
path('soil-prediction-form/', viewszone.soil_prediction_form, name='soil_prediction_form'),
    
   
 

  path('ressource_list/', ressourceview.ressource_list, name='ressource_list'),
    path('ressource/<int:pk>/', ressourceview.ressource_detail, name='ressource_detail'),
    path('ressource/new/', ressourceview.ressource_create, name='ressource_create'),
    path('ressource/<int:pk>/edit/', ressourceview.ressource_update, name='ressource_update'),
    path('ressource/<int:pk>/delete/', ressourceview.ressource_delete, name='ressource_delete'),
    path('search/', ressourceview.ressource_search, name='ressource_search'),

    path('fournisseurs/', ressourceview.fournisseur_list, name='fournisseur_list'),
    path('fournisseurs/<int:pk>/', ressourceview.fournisseur_detail, name='fournisseur_detail'),
    path('fournisseurs/new/', ressourceview.fournisseur_create, name='fournisseur_create'),
    path('fournisseurs/<int:pk>/edit/', ressourceview.fournisseur_update, name='fournisseur_update'),
    path('fournisseurs/<int:pk>/delete/', ressourceview.fournisseur_delete, name='fournisseur_delete'),
     path('predict/', ressourceview.predict_view, name='predict'),

  path("", include("apps.home.urls"))
]
