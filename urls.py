from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
	url(r'^manual_app/', include('manual_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('webapp.urls', namespace='webapp')),
]
