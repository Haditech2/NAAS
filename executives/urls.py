from django.urls import path
from .views import national_executives

urlpatterns = [
    path('national/', national_executives, name='national_executives'),
] 