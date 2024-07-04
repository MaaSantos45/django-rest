from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
