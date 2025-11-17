from django.urls import path
from design_requests import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.DesignRequestCreateView.as_view(), name='create_design_request'),
    path('my/', views.MyDesignRequestsView.as_view(), name='my_design_requests'),
    path('<int:pk>/delete/', views.DesignRequestDeleteView.as_view(), name='delete_design_request'),
]