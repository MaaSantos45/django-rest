from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeHomeView.as_view(), name='home'),
    path('recipes/search/', views.RecipeSearchView.as_view(), name='search'),
    path('category/<int:id_category>/', views.RecipeHomeView.as_view(), name='category'),
    path('recipe-details/<int:id_recipe>/', views.RecipeDetailView.as_view(), name='recipe_details'),
]
