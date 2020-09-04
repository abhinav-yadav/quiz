from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import Home,about,Setting

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('profile/',include('profiles.urls')),
    path('admin/', admin.site.urls),
    path('quiz/', include("core.urls")),
    path('about/', about , name = 'about'),
    path('settings/', Setting.as_view(), name='setting'),
    path('', Home.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
