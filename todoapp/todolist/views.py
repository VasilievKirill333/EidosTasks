from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Task, Project
from .forms import TaskCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todolist/task_list.html"
    login_url = '/login'

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
    return redirect("AboutTask", pk=pk)

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
        context['project_tasks_list'] = Task.objects.filter(project=ss)
        return context




