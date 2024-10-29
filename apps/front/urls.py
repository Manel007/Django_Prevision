from django.urls import path, re_path
from . import views

urlpatterns = [
    path('homeclient/', views.homeF, name='homeF'),
]


