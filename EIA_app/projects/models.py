from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from .chapter import CHAPTERS


class Project(models.Model):
    # metadata
    title = models.CharField(max_length=120)  # max_length
    description = models.TextField(blank=True, null=True, default='U ovoj studiji obrađuju se utjecaji...')
    summary = models.TextField(blank=False, null=False, default='Sažetak studije: Ovo je studija koja se bavi...!')
    active = models.BooleanField(default=False, null=False)

    biology = models.BooleanField(default=False)
    geology = models.BooleanField(default=False)
    forestry = models.BooleanField(default=False)
    climate = models.BooleanField(default=False)
    land_use = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("project:project_detail", kwargs={"id": self.id})  # f'{self.id}/'

    def validate_geo_file_extension(value):
        if not value.name.endswith('.kml'):
            raise ValidationError(u'File is not a .kml')
        if value.name.endswith('.php'):  # php files should definitely not be uploaded or executed
            raise ValidationError(u'Definitely not a shapefile')

    geo_file = models.FileField(upload_to='uploaded_files',
                                validators=[validate_geo_file_extension],
                                blank=True,
                                null=True)

    def get_chapters(self):
        return Chapter.objects.create(project=self)

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the project is being created or updated
        super().save(*args, **kwargs)

        if not created:  # Update chapters only for existing projects
            chapters = [
                ('Biology', self.biology),
                ('Geology', self.geology),
                ('Forestry', self.forestry),
                ('Climate', self.climate),
                ('Land Use', self.land_use),
            ]

            existing_chapters = self.chapters.all()
            existing_chapter_names = set(existing_chapters.values_list('name', flat=True))

            # Add new chapters
            for chapter_name, exists in chapters:
                if exists and chapter_name not in existing_chapter_names:
                    Chapter.objects.create(project=self, name=chapter_name)
                    existing_chapter_names.add(chapter_name)

            # Remove deleted chapters
            for chapter in existing_chapters:
                if chapter.name not in existing_chapter_names:
                    chapter.delete()


class Chapter(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='chapters')
    name = models.CharField(max_length=120, default="chapter_name")
    chapter_intro_text = models.TextField(blank=True, null=True)
    chapter_impact_text = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("project:chapter_list", kwargs={"id": self.id})