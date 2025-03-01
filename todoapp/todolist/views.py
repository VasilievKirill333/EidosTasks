from pydoc import describe

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Task, Project
from .forms import TaskCreationForm, ProjectCreationForm, RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth import login
from django.utils.timezone import now

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import RegisterForm

# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todolist/task_list.html"
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(user=self.request.user)

        # Добавляем `remaining_time` как атрибут к объекту Task
        for task in tasks:
            task.remaining_time = task.time_remaining_dict()  # Добавляем атрибут времени

        context['uncompleted_tasks'] = [
            {"id": task.id, "title": task.title, "priority": task.priority,
             "remaining_time": task.time_remaining_dict()}
            for task in tasks if not task.is_completed
        ]

        context['completed_tasks'] = tasks.filter(is_completed=True)
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "todolist/task_create.html"
    login_url = '/login'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = reverse_lazy("TaskList")


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "todolist/task_update.html"
    login_url = '/login'
    success_url = reverse_lazy("TaskList")
    form_class = TaskCreationForm


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("TaskList")
    login_url = '/login'
    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)


class Login(LoginView):
    template_name = "todolist/login.html"
    success_url = reverse_lazy("TaskList")


class AboutTask(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "todolist/about_task.html"
    login_url = "/login"


def complete(request, pk):
    current = Task.objects.get(id=pk)
    current.is_completed = True
    current.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def incomplete(request, pk):
    current = Task.objects.get(id=pk)
    current.is_completed = False
    current.save()
    return redirect("AboutTask", pk=pk)


class ProjectListView(ListView):
    template_name = 'todolist/project_list.html'
    model = Project
    context_object_name = 'object_list'


class ProjectDetail(DetailView):
    template_name = 'todolist/project_detail.html'
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ss = Project.objects.get(id=self.kwargs['pk'])
        pro_tas_lis = Task.objects.filter(project=ss).order_by('priority', 'date')
        context['project_tasks_list'] = pro_tas_lis
        return context

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'todolist/project_create.html'
    success_url = '/project/'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('TaskList')
    else:
        form = RegisterForm()

    return render(request, 'todolist/register.html', {'form': form})

def set_deadline(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(id=pk)
        task.deadline = request.POST.get('deadline')
        task.save()
        return redirect('TaskList')
    else:
        return render(request, 'todolist/set_deadline.html')






