from django.conf.urls import *
from django.contrib import admin

admin.autodiscover()
urlpatterns = [
	url(r'^manual_app/', include('manual_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('webapp.urls')),
]
