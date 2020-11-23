from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.userLoginView.as_view(), name='login'),
    path('signup/', views.userRegister.as_view(), name='signup'),
    path('complete/', views.registComplete.as_view(), name='complete')
]
