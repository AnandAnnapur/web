# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),  # This already includes 'api/' prefix
    path('admin/', admin.site.urls),
]