from django.conf.urls import url, include, handler404, handler500
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'),
        name='index'),
    
]