from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # или куда нужно
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})