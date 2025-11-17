from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .forms import CustomUserCreationForm, DesignRequestForm
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

class DesignRequestCreateView(LoginRequiredMixin, CreateView):
    model = DesignRequest
    form_class = DesignRequestForm
    template_name = 'design_requests/designrequest_form.html'
    success_url = reverse_lazy('my_design_requests')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'н'
        return super().form_valid(form)

class MyDesignRequestsView(LoginRequiredMixin, ListView):
    model = DesignRequest
    template_name = "design_requests/my_requests.html"
    context_object_name = 'requests'

    def get_queryset(self):
        queryset = DesignRequest.objects.filter(user=self.request.user)
        status = self.request.GET.get('status')

        if status in dict(DesignRequest.STATUS_CHOICES):
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        context['STATUS_CHOICES'] = DesignRequest.STATUS_CHOICES
        return context

class DesignRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = DesignRequest
    template_name = 'design_requests/designrequest_confirm_delete.html'
    success_url = reverse_lazy('my_design_requests')

    def get_queryset(self):
        return DesignRequest.objects.filter(user=self.request.user).filter(status='н')