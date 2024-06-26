from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/search/', views.search, name='search'),
    path('category/<int:id_category>/', views.home, name='category'),
    path('recipe-details/<int:id_recipe>/', views.recipe_detail, name='recipe_details'),
]
