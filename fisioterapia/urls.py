"""
URL configuration for fisioterapia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from fisioterapia.views import dashboard_view

urlpatterns = [
    # Autenticación
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard
    path('', dashboard_view, name='dashboard'),

    # Aplicaciones
    path('pacientes/', include('pacientes.urls')),
    path('citas/', include('citas.urls')),
    path('historiaclinica/', include('historiaclinica.urls')),
    path('tratamientos/', include('tratamientos.urls')),

    # Admin
    path('admin/', admin.site.urls),
]

# Media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
