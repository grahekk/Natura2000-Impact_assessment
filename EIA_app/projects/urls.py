from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('<int:id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('home/', views.ProjectListView.as_view(), name='project_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:id>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:id>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('<int:id>/chapter/', views.ChapterListView.as_view(), name='chapter_list'),
    path('<int:project_id>/chapter/update/<int:chapter_id>/', views.ChapterUpdateView.as_view(), name='chapter_update'),

]
