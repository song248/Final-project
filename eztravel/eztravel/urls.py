"""eztravel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# from travel.views import *
import travel.views
from travel import views
from django.conf.urls import url

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    # url(r'^$', views.index, name = 'index'),
    path('', travel.views.index, name = 'index'),
    # url(r'^howto/', views.howto, name='howto'),
    path('howto/', travel.views.howto, name='howto'),
    path('know/', travel.views.know, name='know'),
    path('login/', travel.views.login, name='login'),
    path('upload/', travel.views.upload, name='upload'),
]


