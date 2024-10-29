from django.urls import path, re_path
from . import views
urlpatterns = [
    path('description/', views.generate_image_from_txt, name='generate_image_from_txt'),
   
]