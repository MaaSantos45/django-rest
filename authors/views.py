from django.shortcuts import render, redirect
from django.http import Http404
from django.core import exceptions as exp
from django.urls import reverse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from recipes import models as recipe_models
from utils.pagination import make_pagination
from . import forms
# Create your views here.


def register(request):
    form = forms.AuthorRegisterForm(request.POST or None)

    if form.errors:
        for field, errors in form.errors.items():
            if field == '__all__':
                field = 'fields'
            messages.error(request, f"{field}: {', '.join(errors)}")

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Successfully Registered')
        return redirect('authors:login')

    return render(request, 'authors/pages/register.html', context={'form': form, 'form_action': reverse('authors:register')})


def login(request):
    form = forms.AuthorLoginForm(request.POST or None)

    if form.errors:
        for field, errors in form.errors.items():
            if field == '__all__':
                field = 'fields'
            messages.error(request, f"{field}: {', '.join(errors)}")

    if request.method == 'POST' and form.is_valid():
        user = auth.authenticate(
            request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )

        if user:
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            return redirect(reverse('recipes:home'))
        messages.error(request, 'Invalid Credentials')

    return render(request, 'authors/pages/login.html', context={'form': form, 'form_action': reverse('authors:login')})


@login_required(login_url='authors:login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logout Successful')
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login')
def profile(request):
    recipes = recipe_models.Recipe.objects.filter(author=request.user).order_by('-created_at').order_by('-updated_at')
    page_obj, pagination_range = make_pagination(request, recipes)
    return render(request, 'authors/pages/profile.html', context={'recipes': page_obj, 'pagination_range': pagination_range})


@login_required(login_url='authors:login')
def create_recipe(request):

    form = forms.AuthorRecipeForm(data=request.POST or None, files=request.FILES or None)

    if form.errors:
        for field, errors in form.errors.items():
            if field == '__all__':
                field = 'fields'
            messages.error(request, f"{field}: {', '.join(errors)}")

    if request.method == 'POST' and form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.is_published = False
        recipe.preparation_steps_is_html = False

        recipe.cover = request.FILES.get('cover')

        recipe.save()
        messages.success(request, 'Recipe Created, wait until review')
        return redirect(reverse('authors:profile'))

    return render(request, 'authors/pages/recipe-detail.html', context={'form': form})


@login_required(login_url='authors:login')
def edit_recipe(request, id_recipe):
    recipe = recipe_models.Recipe.objects.filter(id=id_recipe, author=request.user).first()
    if not recipe:
        raise Http404('No recipe found')

    form = forms.AuthorRecipeForm(data=request.POST or None, files=request.FILES or None, instance=recipe)

    if form.errors:
        for field, errors in form.errors.items():
            if field == '__all__':
                field = 'fields'
            messages.error(request, f"{field}: {', '.join(errors)}")

    if request.method == 'POST' and form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.is_published = False
        recipe.preparation_steps_is_html = False

        recipe.cover = request.FILES.get('cover')

        recipe.save()
        messages.success(request, 'Recipe updated, wait until review')
        return redirect(reverse('authors:profile'))

    if recipe.is_published:
        messages.warning(request, "Recipe already published, if you update, it'll be unpublished for review")

    return render(request, 'authors/pages/recipe-detail.html', context={"recipe": recipe, 'form': form})


@login_required(login_url='authors:login')
def delete_recipe(request, id_recipe):
    recipe = recipe_models.Recipe.objects.filter(id=id_recipe, author=request.user).first()
    if not recipe:
        raise Http404('No recipe found')

    if request.method == 'POST' and recipe.author == request.user:
        recipe.delete()
        messages.success(request, 'Recipe deleted')

    return redirect(reverse('authors:profile'))
