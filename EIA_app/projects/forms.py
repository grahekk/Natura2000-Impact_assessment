from django import forms
from django.forms import FileInput

from .models import Project, Chapter


class CustomClearableFileInput(FileInput):
    template_name = 'projects/custom_clearable_file_input.html'


class ProjectForm(forms.ModelForm):
    geo_file = forms.FileField(allow_empty_file=True)#, widget=CustomClearableFileInput(attrs={'class': 'button'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['geo_file'].widget.attrs['class'] = 'button'

    class Meta:
        model = Project
        fields = ['title', 'description', 'summary','biology','geology','forestry','climate','land_use']


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_intro_text', 'chapter_impact_text']
