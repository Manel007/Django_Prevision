from django.urls import path
from . import views
from .views import yield_prediction_view



urlpatterns = [
    path('list/', views.yield_list, name='yield_list'),
    path('yield/<int:pk>/', views.yield_detail, name='yield_detail'),
    path('yield/new/', views.yield_create, name='yield_create'),
    path('yield/<int:pk>/edit/', views.yield_update, name='yield_update'),
    path('yield/<int:pk>/delete/', views.yield_delete, name='yield_delete'),
   
    path('yield/prediction/', yield_prediction_view, name='yield_prediction'),
]

