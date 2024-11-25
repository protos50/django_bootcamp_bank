"""
URL configuration for bank_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='landing'),
    path('users/', include('apps.users.urls')),
    path('transactions/', include('apps.transactions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
