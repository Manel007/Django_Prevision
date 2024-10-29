from django.urls import path
from . import views
from .views import yield_prediction_view
from .views import yield_classification_view  # Importez la vue
from .views import create_review
from .views import review_list  # Import the view
from .views import yield_summary  # Import the view
from .views import crop_classification_view

urlpatterns = [
    path('list/', views.yield_list, name='yield_list'),  # URL with no arguments
    path('summary/', views.yield_summary, name='yield_summary'),  # Summary page
    path('review/create/<int:yield_id>/', views.create_review, name='create_review'),
    path('previous/', views.crop_classification_view, name='crop_classification_view'),

    path('yield/<int:pk>/', views.yield_detail, name='yield_detail'),
    path('yield/new/', views.yield_create, name='yield_create'),
    path('yield/<int:pk>/edit/', views.yield_update, name='yield_update'),
    path('yield/<int:pk>/delete/', views.yield_delete, name='yield_delete'),
    path('yield/<int:yield_id>/reviews/', review_list, name='review_list'),  # Example URL pattern
    path('review/<int:pk>/update/', views.review_update, name='review_update'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('yield-classification/', yield_classification_view, name='yieldd_classification'),

    # Review URLs


    path('yield/prediction/', yield_prediction_view, name='yield_prediction'),

]

