# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user 
from django.contrib.auth.views import LogoutView
from .views import culture_create, culture_update, culture_delete, culture_list

urlpatterns = [
  path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),  # Registration URL
    path("logout/", LogoutView.as_view(), name="logout"), 
    path('cultures/', culture_list, name='culture_list'),
    path('cultures/create/', culture_create, name='culture_create'),
    path('cultures/update/<int:culture_id>/', culture_update, name='culture_update'),
    path('culture/delete/<int:culture_id>/', culture_delete, name='culture_delete'),












]
