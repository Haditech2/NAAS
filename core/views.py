from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.template import RequestContext
from django.views.generic import ListView, DetailView

# Import models from other apps
from events.models import Event
from .models import News, Executive, Testimonial
from executives.models import Executive
from chapters.models import Chapter

# Import forms
from .forms import ContactForm


def handler404(request, exception, template_name='404.html'):
    """
    Custom 404 error handler
    """
    response = render(request, template_name, status=404)
    response.status_code = 404
    return response


def handler500(request, template_name='500.html'):
    """
    Custom 500 error handler
    """
    response = render(request, template_name, status=500)
    response.status_code = 500
    return response

# News Views
class NewsListView(ListView):
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-published_date')

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        return News.objects.filter(is_published=True)

# Executive Views
class ExecutiveListView(ListView):
    model = Executive
    template_name = 'executives/list.html'
    context_object_name = 'executives'
    
    def get_queryset(self):
        return Executive.objects.filter(is_current=True).order_by('position')

# Testimonial Views
class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/list.html'
    context_object_name = 'testimonials'
    
    def get_queryset(self):
        return Testimonial.objects.filter(is_featured=True).order_by('-created_date')

def home(request):
    """
    Home page view
    """
    # Get upcoming events (limit to 3)
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:3]
    
    # Get latest news (limit to 3)
    latest_news = News.objects.filter(is_published=True).order_by('-published_date')[:3]
    
    # Get featured testimonials (limit to 5)
    featured_testimonials = Testimonial.objects.filter(is_featured=True).order_by('-created_date')[:5]
    
    national_executives = Executive.objects.filter(level='national')
    for exco in national_executives:
        if exco.photo:
            exco.photo_name = exco.photo.name.split('/')[-1]
        else:
            exco.photo_name = ''
    chapters = Chapter.objects.all()
    context = {
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
        'featured_testimonials': featured_testimonials,
        'national_executives': national_executives,
        'chapters': chapters,
    }
    return render(request, 'home.html', context)

def about(request):
    """
    About page view
    """
    return render(request, 'about.html')

def contact(request):
    """
    Contact page view with form submission
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            department = form.cleaned_data['department']
            message = form.cleaned_data['message']
            
            # Send email (in production, you would use Celery or similar for async)
            email_subject = f"New Contact Form Submission: {subject}"
            email_message = f"""
            Name: {name}
            Email: {email}
            Department: {department}
            
            Message:
            {message}
            """
            
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],  # Add this to your settings
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message. We will get back to you soon!')
                return redirect('contact')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again later.')
                # Log the error in production
                print(f"Error sending email: {e}")
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
