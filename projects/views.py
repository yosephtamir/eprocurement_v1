from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Project

class ProjectDetail(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = "projects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "On Going Project"

        return context

class ProjectList(ListView):
    template_name = 'projects/project_list.html'
    model = Project
    context_object_name = 'projects'
    ordering = ['-updated_at']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "On Going Projects"

        return context