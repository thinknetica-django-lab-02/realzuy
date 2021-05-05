from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Strategy


class StrategySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Strategy.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.date_modify
