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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from travel import views
from django.conf.urls import url
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^$', views.index, name = 'index'),
    # url(r'^howto/', views.howto, name='howto'),

    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('main/', views.mainview.as_view(), name='main'),
    path('howto/', views.howto, name='howto'),
    path('know/', views.know, name='know'),
    #path('login/', user.views.LoginView, name='login'),
    #path('login/', include('user.urls', 'login'), name='login'),
    path('login/', include('account.urls', 'login')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('getmap/', views.getmap, name='getmap'),
    # path('know/post/<int:id>', travel.views.know_show)
    url(r'^post/(?P<pk>\d+)/', views.know_show), 
    url(r'^uimage/$', views.uimage, name='uimage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

"""
beforeSend
complete
"""