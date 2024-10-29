from django.urls import path, re_path
from . import views


urlpatterns = [
    path('add/', views.add_prog, name='add_prog'),
    path('all/', views.all_prog, name='all_prog'),
    path('<int:pk>/delete', views.delete_prog, name='delete_prog'),
    path('<int:pk>/edit/', views.edit_prog, name='edit_prog'),
    path('<int:pk>/details/', views.details_prog, name='details_prog'),

    # front
    path('clientprogs/', views.front_prog, name='front_prog'),


]


