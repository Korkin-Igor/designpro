from django.urls import path
from design_requests import views

urlpatterns = [
    # Гость
    path('', views.index, name='index'),

    # Юзер
    path('create/', views.DesignRequestCreateView.as_view(), name='create_design_request'),
    path('my/', views.MyDesignRequestsView.as_view(), name='my_design_requests'),
    path('<int:pk>/delete/', views.DesignRequestDeleteView.as_view(), name='delete_design_request'),

    # Админка
    path('admin/requests/', views.AllDesignRequestsView.as_view(), name='all_design_requests'),
    path(
        '<int:pk>/set-status/working/',
        views.DesignRequestSetStatusView.as_view(),
        {'target_status': 'п'},
        name='set_status_working'
    ),
    path(
        '<int:pk>/set-status/done/',
        views.DesignRequestSetStatusView.as_view(),
        {'target_status': 'в'},
        name='set_status_done'
    ),
    path('admin/categories/', views.CategoryListView.as_view(), name='categories'),
    path('admin/categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('admin/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]