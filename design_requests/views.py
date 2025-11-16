from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import DesignRequest


def index(request):
    design_requests = DesignRequest.objects.filter(status='в').order_by('created_at')
    paginator = Paginator(design_requests, 4)  # 4 заявки на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj,}
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})