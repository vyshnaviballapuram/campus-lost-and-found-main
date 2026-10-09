"""
URL configuration for campusLostAndFound project.
Yeh main URL configuration file hai jo sab URLs ko route karti hai.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Main URL patterns - sab URLs yahan define hain
urlpatterns = [
    # Admin panel ka URL
    path('admin/', admin.site.urls),
    
    # Items app ke URLs include kar rahe hain
    path('', include('items.urls')),
    
    # Django built-in authentication URLs (login, logout, password reset)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Development mein media files serve karne ke liye
# Production mein nginx/apache use karna chahiye
from django.views.static import serve
from django.urls import re_path
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]