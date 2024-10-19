
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('list/', views.list_agriculteurs, name='list_agriculteurs'),
    path('create/', views.create_agriculteurs, name='create_agriculteurs'),
    path('agriculteurs/edit/<int:agriculteur_id>/', views.edit_agriculteur, name='edit_agriculteur'), 
    path('agriculteurs/delete/<int:agriculteur_id>/', views.delete_agriculteur, name='delete_agriculteur'),

]
