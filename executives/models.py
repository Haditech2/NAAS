from django.db import models
from chapters.models import Chapter

# Create your models here.

class Executive(models.Model):
    LEVEL_CHOICES = (
        ('national', 'National'),
        ('chapter', 'Chapter'),
    )
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='executives/')
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} ({self.role})"
