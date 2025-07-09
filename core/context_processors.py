from django.conf import settings

def site_info(request):
    """
    Add site-wide information to the template context.
    """
    return {
        'SITE_NAME': 'National Association of Ankpa Students',
        'SITE_URL': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
        'DEBUG': settings.DEBUG,
    }

def navigation_links(request):
    """
    Add navigation links to the template context.
    """
    return {
        'nav_links': [
            {'name': 'Home', 'url': 'core:home', 'icon': 'fas fa-home'},
            {'name': 'About', 'url': 'core:about', 'icon': 'fas fa-info-circle'},
            {'name': 'Events', 'url': 'events:event_list', 'icon': 'fas fa-calendar-alt'},
            {'name': 'Gallery', 'url': 'gallery:gallery', 'icon': 'fas fa-images'},
            {'name': 'Forum', 'url': 'forum:forum_list', 'icon': 'fas fa-comments'},
            {'name': 'Contact', 'url': 'core:contact', 'icon': 'fas fa-envelope'},
        ],
    }

def social_links(request):
    """
    Add social media links to the template context.
    """
    return {
        'social_links': [
            {'name': 'Facebook', 'url': 'https://facebook.com/ankpastudents', 'icon': 'fab fa-facebook-f'},
            {'name': 'Twitter', 'url': 'https://twitter.com/ankpastudents', 'icon': 'fab fa-twitter'},
            {'name': 'Instagram', 'url': 'https://instagram.com/ankpastudents', 'icon': 'fab fa-instagram'},
            {'name': 'LinkedIn', 'url': 'https://linkedin.com/company/ankpa-student-association', 'icon': 'fab fa-linkedin-in'},
            {'name': 'YouTube', 'url': 'https://youtube.com/ankpastudents', 'icon': 'fab fa-youtube'},
        ],
    }
