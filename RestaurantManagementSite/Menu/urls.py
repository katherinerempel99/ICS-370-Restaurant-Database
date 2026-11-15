from django.urls import path
from . import views # import views from current directory

# Define a list of URL patterns
urlpatterns = [
    path('', views.index),
    path('recipe/', views.recipe_detail),
]