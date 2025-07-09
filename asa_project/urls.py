"""
URL configuration for asa_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Core app
    path('', include('core.urls', namespace='core')),
    
    # Accounts app (authentication)
    path('accounts/', include('accounts.urls', namespace='accounts')),
    
    # Events app
    path('events/', include('events.urls', namespace='events')),
    
    # Gallery app
    path('gallery/', include('gallery.urls', namespace='gallery')),
    
    # Forum app
    path('forum/', include('forum.urls', namespace='forum')),

    # Chapters app
    path('chapters/', include('chapters.urls')),

    # Executives app
    path('executives/', include('executives.urls')),
    
    # Django Allauth URLs (for social authentication)
    path('accounts/', include('allauth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
