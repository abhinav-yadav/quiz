from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include("core.urls")),
    path('home/', Home.as_view(), name='home'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, documen_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, documen_root = settings.MEDIA_ROOT)