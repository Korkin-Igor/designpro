from itertools import count

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import DesignRequest


def index(request):
    design_requests = DesignRequest.objects.filter(status__exact='в').all()
    context = {
        'design_requests': design_requests
    }
    return render(request, 'index.html', context=context)

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