from django.contrib import admin
from django.urls import path, include
from user import views
from . import views

app_name = 'user'

urlpatterns = [
    # path('', views.uLoginView.as_view(), name='login'),
    path('', views.UserLoginView.as_view(), name='login'),

    path('regist/', views.uRegister.as_view(), name='regist'),
    path('complete/', views.uComplete.as_view(), name='complete'),
    
    path('logout/', views.logout, name='logout'),
    path('find_id/', views.find_id, name='find_id'),
    path('find_pw/', views.find_pw, name='find_pw'),
    path('main/', views.main, name='main'),
    
    path('signup', views.signup, name='signup'),
]
