from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import TaskForm
from .mixins import UserIsOwnerMixin
from .models import Task

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks' 

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
