from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from design_requests.models import CustomUser


def index(request):
    return render(request, 'index.html')

class CustomUserCreate(CreateView):
    model = CustomUser
    fields = '__all__'