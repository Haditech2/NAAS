from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import landscape
IDCARD = (3.37 * 72, 2.13 * 72)  # width, height in points
from reportlab.pdfgen import canvas
import io
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.staticfiles import finders
from reportlab.lib.utils import ImageReader
from django.conf import settings
import os
from core.models import Executive

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Send activation email
            current_site = get_current_site(request)
            subject = 'Activate Your NAAS Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, None, [user.email])
            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('accounts:login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def generate_id_card(request):
    user = request.user
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(IDCARD))
    # Draw ID card background
    p.setFillColorRGB(0.95, 0.95, 1)
    p.rect(0, 0, 336, 210, fill=1)
    # Draw user details
    p.setFont('Helvetica-Bold', 16)
    p.drawString(20, 180, f"{user.first_name} {user.last_name}")
    p.setFont('Helvetica', 12)
    p.drawString(20, 160, f"School: {user.school}")
    p.drawString(20, 140, f"Level: {user.level}")
    p.drawString(20, 120, f"Department: {user.department}")
    p.drawString(20, 100, f"Phone: {user.phone}")
    p.drawString(20, 80, f"LGA/Ward: {user.lga_ward}")
    p.drawString(20, 60, f"Email: {user.email}")
    # Optionally, add a placeholder for photo
    p.setStrokeColorRGB(0.7, 0.7, 0.7)
    p.rect(250, 80, 60, 80, fill=0)
    p.setFont('Helvetica', 8)
    p.drawString(252, 75, "Passport")
    # Draw logo if available
    logo_path = finders.find('images/logo.png')
    if logo_path:
        p.drawImage(logo_path, 10, 150, 60, 40, mask='auto')  # Adjust position/size as needed
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="naas_id_card.pdf"'
    return response

@login_required
def generate_executive_id_card(request):
    try:
        executive = request.user.executive_profile
    except Executive.DoesNotExist:
        return HttpResponse('You are not registered as an executive.', status=403)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="executive_id_card.pdf"'

    # ID card size (landscape credit card size)
    width, height = 336, 210  # 3.37 x 2.125 inches at 100 dpi
    p = canvas.Canvas(response, pagesize=(width, height))

    # Draw background
    p.setFillColorRGB(0.95, 0.95, 1)
    p.rect(0, 0, width, height, fill=1)

    # Draw logo (top left)
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 10, height-60, width=50, height=50, mask='auto')

    # Draw photo (left side)
    if executive.photo and hasattr(executive.photo, 'path') and os.path.exists(executive.photo.path):
        p.drawImage(executive.photo.path, 10, 60, width=60, height=80, mask='auto')
    else:
        # Placeholder rectangle if no photo
        p.setFillColorRGB(0.8, 0.8, 0.8)
        p.rect(10, 60, 60, 80, fill=1)
        p.setFillColorRGB(0, 0, 0)
        p.drawString(20, 100, 'No Photo')

    # Name
    p.setFont('Helvetica-Bold', 14)
    p.drawString(80, height-40, f"{request.user.get_full_name()}")

    # Position or Member
    position = dict(Executive.POSITION_CHOICES).get(executive.position, 'Member')
    p.setFont('Helvetica', 12)
    p.drawString(80, height-60, f"Position: {position if executive.position else 'Member'}")

    # ID label
    p.setFont('Helvetica-Bold', 10)
    p.drawString(10, 20, 'National Association of Ankpa Students (NAAS)')
    p.setFont('Helvetica', 9)
    p.drawString(10, 8, 'Executive ID Card')

    p.showPage()
    p.save()
    return response

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')

class UserLogoutView(LogoutView):
    next_page = '/'

User = get_user_model()

class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'school', 'level', 'department', 'phone', 'lga_ward', 'profile_picture']

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = StudentProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = StudentProfileEditForm(instance=user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

class StudentPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')

class StudentPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/accounts/login/'

class StudentPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = '/accounts/login/'

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('accounts:login')
