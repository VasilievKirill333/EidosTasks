from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Task, Project
from .forms import TaskCreationForm, ProjectCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils.timezone import now

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
        context['uncompleted_tasks'] = Task.objects.filter(Q(user=self.request.user) & \
                                                           Q(is_completed = False))
        context['completed_tasks'] = Task.objects.filter(Q(user=self.request.user) & Q(is_completed = True))
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




