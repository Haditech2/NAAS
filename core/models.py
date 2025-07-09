from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class News(models.Model):
    """
    Model for news articles on the website
    """
    CATEGORY_CHOICES = [
        ('general', 'General News'),
        ('events', 'Event Updates'),
        ('scholarship', 'Scholarships'),
        ('achievements', 'Student Achievements'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='news_articles')
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    featured_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


class Executive(models.Model):
    """
    Model for executive team members
    """
    POSITION_CHOICES = [
        ('president', 'President'),
        ('vice_president', 'Vice President'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('publicity', 'Publicity Secretary'),
        ('welfare', 'Welfare Officer'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='executive_profile')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='executives/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_position_display()}"


class Testimonial(models.Model):
    """
    Model for student testimonials
    """
    author = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"Testimonial by {self.author}"
