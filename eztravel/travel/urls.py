from django.contrib import admin
from django.urls import path
from travel import views
# from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.mainview.as_view(), name='main'),
    path('upload/', views.upload, name='upload'),
]