from django.urls import path
from . import views, class_views

app_name = 'recipes'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', class_views.RecipeHomeView.as_view(), name='home'),
    # path('recipes/search/', views.search, name='search'),
    path('recipes/search/', class_views.RecipeSearchView.as_view(), name='search'),
    # path('category/<int:id_category>/', views.home, name='category'),
    path('category/<int:id_category>/', class_views.RecipeHomeView.as_view(), name='category'),
    # path('recipe-details/<int:id_recipe>/', views.recipe_detail, name='recipe_details'),
    path('recipe-details/<int:id_recipe>/', class_views.RecipeDetailView.as_view(), name='recipe_details'),
]
