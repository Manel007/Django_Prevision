# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user 
from django.contrib.auth.views import LogoutView
from .views import culture_create, culture_update, culture_delete, culture_list
from .views import predict_yield  # Import the view
from .views import temperature_prediction_view  # Importez la vue
from .views import pre_yield

urlpatterns = [
  path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),  # Registration URL
    path("logout/", LogoutView.as_view(), name="logout"), 
    path('pre_yield/', predict_yield, name='pre_yield'),  # Add this line
    path('predict-temperature/', temperature_prediction_view, name='predict_temperature'),


    path('predict_yield/', predict_yield, name='predict_yield'),
    path('cultures/', culture_list, name='culture_list'),
    path('cultures/create/', culture_create, name='culture_create'),
    path('cultures/update/<int:culture_id>/', culture_update, name='culture_update'),
    path('culture/delete/<int:culture_id>/', culture_delete, name='culture_delete'),












]
