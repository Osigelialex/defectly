from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False)),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('projects/', views.project_view, name='projects'),
    path('bugs/', views.bugs_view, name='bug_view'),
    path('administration/', views.administration, name='administration'),
    path('project/<int:id>', views.project_info_view, name='project_info'),
    path('bug_info/<int:id>', views.bug_info, name='bugInfo')
]