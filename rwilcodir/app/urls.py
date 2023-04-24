from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.current_training_view, name='current_training'),
    path('training_search/', views.training_search_view, name='training_search'),
    path('employee_search/', views.employee_search_view, name='employee_search'),
    path('supervisor/', views.supervisor_view, name='supervisor'),
    path('help/', views.help_view, name='help_view'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
