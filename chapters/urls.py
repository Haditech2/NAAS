from django.urls import path
from .views import chapter_list, chapter_detail

urlpatterns = [
    path('', chapter_list, name='chapter_list'),
    path('<int:pk>/', chapter_detail, name='chapter_detail'),
] 