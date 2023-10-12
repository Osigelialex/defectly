from django.urls import path
from . import views


urlpatterns = [
    path('projects/', views.project_view, name='projects'),
    path('project/<int:id>', views.project_info_view, name='project_info'),
]