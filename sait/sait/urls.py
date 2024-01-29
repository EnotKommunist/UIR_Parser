"""
URL configuration for sait project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from pars_sait.views import index_page, input_page, parse_page, print_db


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', index_page),
    path('', input_page, name='input_page'),
    path('parse/', parse_page, name='parse_page'),
    path('print_db/', print_db, name='print_db'),
]
