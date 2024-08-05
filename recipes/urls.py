from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeHomeView.as_view(), name='home'),
    path('recipes/api/v1/', views.RecipeHomeViewApi.as_view(), name='home_api'),
    path('recipes/search/', views.RecipeSearchView.as_view(), name='search'),
    path('category/<int:id_category>/', views.RecipeHomeView.as_view(), name='category'),
    path('tags/<slug:slug>/', views.RecipeTagView.as_view(), name='tag'),
    path('recipe-details/<int:id_recipe>/', views.RecipeDetailView.as_view(), name='recipe_details'),
    path('recipes/api/v1/<int:id_recipe>/', views.RecipeDetailViewApi.as_view(), name='recipe_details_api'),
]
