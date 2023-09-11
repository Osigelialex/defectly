from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('projects/', views.project_view, name='projects'),
    path('project/<int:id>', views.project_info_view, name='project_info'),
    path('add_comment/', views.comments_view, name='comments'),
    path('bug_info/<int:id>', views.bug_info, name='bugInfo')
]