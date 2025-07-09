from django.contrib import admin
from .models import News, Executive, Testimonial

# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_date', 'is_published')
    list_filter = ('category', 'is_published', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)

@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'is_current', 'start_date', 'end_date')
    list_filter = ('position', 'is_current')
    search_fields = ('user__first_name', 'user__last_name', 'position')
    ordering = ('position',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'role', 'is_featured', 'created_date')
    list_filter = ('is_featured', 'created_date')
    search_fields = ('author', 'content')
    ordering = ('-created_date',)
