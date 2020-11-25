from django.urls import path, include
from . import views
from django.conf.urls import include, url

app_name = 'account'

urlpatterns = [
    # url(r'', views.userLoginView.as_view(), name='login'),
    # url(r'^signup/', views.userLoginView.as_view(), name='signup'),
    # url(r'^signup/', views.userLoginView.as_view(), name='signup')
    path('', views.userLoginView.as_view(), name='login'),
    path('signup/', views.userRegister.as_view(), name='signup'),
    path('complete/', views.registComplete.as_view(), name='complete'),
    path('test', views.test, name='test'),
]
