from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        # List of view names to include in the sitemap
        return [
            'core:home',
            'core:about',
            'core:contact',
            'events:event_list',
            'gallery:gallery',
            'forum:forum_list',
        ]

    def location(self, item):
        return reverse(item)
