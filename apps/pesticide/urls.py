from django.urls import path, re_path
from . import views

urlpatterns = [
    
    path('all/', views.all_pesticide, name='all_pesticide'),
    path('newPesticide/', views.pesticide_create, name='pesticide_create'),
    path('pesticie/<int:pk>/edit', views.edit_pesticide, name='edit_pesticide'), 
    path('pesticide/<int:pk>/delete', views.delete_pesticide, name='delete_pesticide'),
    path('pesticide/prediction/<int:pesticide_id>/', views.pesticide_prediction_view, name='pesticide_prediction_view'),
    path('pesticide/predict_all/', views.pesticide_prediction_view, {'predict_all': True}, name='predict_all_pesticides'),
    path('store_selected_pesticides/', views.store_selected_pesticides, name='store_selected_pesticides'),


    path('homepesticide/all/', views.all_pesticideFront, {'predict_allF': True},name='all_pesticideFront'),
    


]


