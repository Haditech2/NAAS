from django.db import models

# Create your models here.

class Chapter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    contact = models.CharField(max_length=100, blank=True)
    picture = models.ImageField(upload_to='chapter_pics/', blank=True, null=True)

    def __str__(self):
        return self.name
