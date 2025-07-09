from django.urls import path
from . import views
from .views import NewsListView, NewsDetailView, ExecutiveListView, TestimonialListView

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # News URLs
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    
    # Executive URLs
    path('executives/', ExecutiveListView.as_view(), name='executive_list'),
    
    # Testimonial URLs
    path('testimonials/', TestimonialListView.as_view(), name='testimonial_list'),
]
