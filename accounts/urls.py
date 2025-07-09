from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('id-card/', views.generate_id_card, name='generate_id_card'),
    path('executive-id-card/', views.generate_executive_id_card, name='executive_id_card'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password/change/', views.StudentPasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', views.StudentPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', views.StudentPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
