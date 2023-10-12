from django.urls import path
from . import views


urlpatterns = [
    path('bugs/', views.bugs_view, name='bug_view'),
    path('bug_info/<int:id>', views.bug_info, name='bugInfo')
]