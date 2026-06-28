from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm, CommentForm
from .models import Task, Comment, Like
from .mixins import UserIsOwnerMixin

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks' 

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        
        task = self.get_object()
        comments = task.comments.all()
        
        if self.request.user.is_authenticated:
            liked_comment_ids = Like.objects.filter(
                user=self.request.user, 
                comment__task=task
            ).values_list('comment_id', flat=True)
            
            for comment in comments:
                comment.is_liked = comment.id in liked_comment_ids

        context['comments'] = comments

        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.creator = request.user
            comment.save()
            return redirect('task-detail', pk=comment.task.pk)

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

class CommentUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Comment
    fields = ['content']
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})
    
class CommentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Comment
    context_object_name = 'comment'
    
    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})
    
def like_comment(request, pk):
    if not request.user.is_authenticated:
        return redirect('task-list')

    comment = get_object_or_404(Comment, id=pk)
    
    like_filter = Like.objects.filter(comment=comment, user=request.user)

    if like_filter.exists():
        like_filter.delete()
    else:
        Like.objects.create(comment=comment, user=request.user)
        
    return redirect(reverse_lazy('task-detail', kwargs={'pk': comment.task.pk}))