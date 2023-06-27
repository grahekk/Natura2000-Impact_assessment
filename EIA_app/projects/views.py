from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView,
                                  DetailView,
                                  ListView,
                                  UpdateView,
                                  DeleteView)

from .forms import ProjectForm
from .models import Project, Chapter
from .chapter import CHAPTERS


class ProjectDetailView(DetailView):
    template_name = 'projects/project_detail.html'
    fields = '__all__'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Project, id=id)

    def get_success_url(self):
        return reverse('project:project_update')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            return render(request, 'projects/project_update.html', {})


class ProjectListView(ListView):
    template_name = 'projects/project_list.html'
    queryset = Project.objects.all()


class ProjectCreateView(CreateView):
    template_name = 'projects/project_create.html'
    queryset = Project.objects.all()
    form_class = ProjectForm

    def form_valid(self, form):
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    template_name = 'projects/project_delete.html'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Project, id=id)

    def get_success_url(self):
        return reverse('project:project_list')


class ProjectUpdateView(UpdateView):
    template_name = 'projects/project_update.html'
    fields = '__all__'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Project, id=id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def upload_file(request):
        if request.method == "POST":
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return reverse_lazy('project:project_detail', kwargs={"id": self.kwargs.get("id")})
            else:
                raise ValidationError

    def get_success_url(self):
        return reverse_lazy('project:project_detail', kwargs={"id": self.kwargs.get("id")})


class ChapterListView(ListView):
    model = Chapter
    template_name = 'projects/chapter_list.html'
    fields = '__all__'
    context_object_name = 'chapters'

    def get_queryset(self):
        project_id = self.kwargs.get('id')
        return Chapter.objects.filter(project_id=project_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('id')
        project = Project.objects.get(id=project_id)
        context['project'] = project
        context['project_id'] = self.kwargs.get('id')
        return context


class ChapterUpdateView(UpdateView):
    model = Chapter
    template_name = 'projects/chapter_update.html'
    fields = ['chapter_intro_text', 'chapter_impact_text']
    context_object_name = 'chapter'

    def get_object(self, queryset=None):
        chapter_id = self.kwargs.get('chapter_id')
        return Chapter.objects.get(id=chapter_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        context['project'] = project
        context['project_id'] = self.kwargs.get('project_id')
        return context

    def get_success_url(self):
        print(self.object.project_id)
        project_id = self.object.project_id
        return reverse_lazy('project:chapter_list', kwargs={'id': project_id})
