from django.urls import path
from .views import (TaskListView, TaskCreate, TaskUpdate, TaskDelete, Login, AboutTask, complete, incomplete,
                    ProjectListView, ProjectDetail, ProjectCreateView, register, set_deadline)
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('', TaskListView.as_view(), name="TaskList"),
    path('create/', TaskCreate.as_view(), name="TaskCreate"),
    path('update/<int:pk>/', TaskUpdate.as_view(), name="TaskUpdate"),
    path('delete/<int:pk>/', TaskDelete.as_view(), name="TaskDelete"),
    path('login/', Login.as_view(), name="Login"),
    path('logout/', LogoutView.as_view(), name="Logout"),
    path('register/', register, name='register'),
    path('abouttask/<int:pk>/', AboutTask.as_view(), name="AboutTask"),
    path('abouttask/<int:pk>/complete/',complete, name="complete" ),
    path('abouttask/<int:pk>/incomplete/', incomplete, name="incomplete"),
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', ProjectDetail.as_view(), name='project_detail'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('task/<int:pk>/set_d', set_deadline, name='set_deadline'),
]
