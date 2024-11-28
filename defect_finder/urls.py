"""
URL configuration for defect_finder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from defect_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inspection_page, name='inspection_page'),
    path('analyze_defect/', views.analyze_defect, name='analyze_defect'),
    path('history/', views.inspection_history, name='inspection_history'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)