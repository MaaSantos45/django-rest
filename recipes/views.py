from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, Http404
from utils.recipes.factory import make_recipes
from . import models

# Create your views here.


def home(request, id_category=None):

    recipes = models.Recipe.objects.all().order_by('-created_at').order_by('-updated_at')
    recipes = recipes.filter(is_published=True)
    if id_category is not None:
        recipes = recipes.filter(category__id=id_category)
    return render(request, "recipes/pages/home.html", context={'recipes': recipes})


def recipe_detail(request, id_recipe):
    recipe = models.Recipe.objects.filter(id=id_recipe, is_published=True).first()
    if not recipe:
        raise Http404('No recipe found')
    return render(request, "recipes/pages/recipe-detail.html", context={"recipe": recipe})


def search(request):
    q_term = request.GET.get('q', '').strip()
    if not q_term:
        return redirect(reverse('recipes:home'))

    recipes = models.Recipe.objects.all().order_by('-created_at').order_by('-updated_at')
    recipes = recipes.filter(is_published=True)
    terms = q_term.split(' ')
    for term in terms:
        recipes = recipes.filter(
            Q(title__icontains=term) |
            Q(slug__icontains=term) |
            Q(description__icontains=term) |
            Q(author__first_name__icontains=term) |
            Q(author__last_name__icontains=term) |
            Q(author__username__icontains=term) |
            Q(category__name__icontains=term)
        )

    return render(request, "recipes/pages/home.html", context={"recipes": recipes, "q_term": q_term})
