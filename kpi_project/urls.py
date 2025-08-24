"""
URL configuration for kpi_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from dashboard import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.dashboard_home_min, name='home'),
    path('upload/', v.upload_csv, name='upload_csv'),
    path('export/csv/', v.export_csv, name='export_csv'),
    path('export/xlsx/', v.export_xlsx, name='export_xlsx'),

    
]
