from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, DesignRequestForm
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import DesignRequest, Category
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import DesignRequestUpdateForm

def index(request):
    design_requests = DesignRequest.objects.filter(status='в').order_by('created_at')
    paginator = Paginator(design_requests, 4)  # 4 заявки на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'count_requests': DesignRequest.objects.filter(status='п').count(),
    }
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

@method_decorator(permission_required('design_requests.can_manage_requests', raise_exception=True), name='dispatch')
class AllDesignRequestsView(ListView):
    model = DesignRequest
    template_name = 'design_requests/all_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        queryset = DesignRequest.objects.all()
        status = self.request.GET.get('status')

        if status in dict(DesignRequest.STATUS_CHOICES):
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        context['STATUS_CHOICES'] = DesignRequest.STATUS_CHOICES
        return context


@method_decorator(permission_required('design_requests.can_manage_requests', raise_exception=True), name='dispatch')
class DesignRequestSetStatusView(LoginRequiredMixin, UpdateView):
    model = DesignRequest
    form_class = DesignRequestUpdateForm
    template_name = 'design_requests/designrequest_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('design_requests.can_manage_requests'):
            raise PermissionDenied("У вас нет прав на управление заявками.")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = self.kwargs.get('target_status')
        return initial

    def get_success_url(self):
        return reverse_lazy('all_design_requests')


@method_decorator(permission_required('design_requests.can_manage_categories', raise_exception=True), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'design_requests/category_list.html'
    context_object_name = 'categories'


@method_decorator(permission_required('design_requests.can_manage_categories', raise_exception=True), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'design_requests/category_form.html'
    success_url = reverse_lazy('categories')


@method_decorator(permission_required('design_requests.can_manage_categories', raise_exception=True), name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')