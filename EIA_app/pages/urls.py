from django.urls import path
from .views import (home_view)

app_name = 'project'
urlpatterns = [
    path('', home_view, name='project-detail'),
]
