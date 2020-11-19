from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import View, CreateView, TemplateView
from .forms import CreateUserForm, SigninForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

class u(LoginView):
    template_name = 'login/login.html'

class uLoginView(LoginView):
    template_name = 'login/login.html'

class uRegister(CreateView):
    template_name = 'login/regist_2.html'
    form_class = CreateUserForm
    success_url = '/login/complete/'

class uComplete(View):
    def get(self, request):
        return render(request, 'login/complete.html')

#-------------------------------------------------------------------------------------------------------
"""def signin(request):    #로그인 기능
    if request.method == "GET":
        return render(request, 'user/login.html', {'f':SigninForm()} )
    elif request.method == "POST":
        form = SigninForm(request.POST)
        id = request.POST['email']
        pw = request.POST['password']
        u = authenticate(username=id, password=pw)
        if u: #u에 특정 값이 있다면
            login(request, user=u) #u 객체로 로그인해라
            return HttpResponseRedirect(reverse('travel:index'))
        else:
            return render(request, 'user/login.html',{'f':form, 'error':'아이디나 비밀번호가 일치하지 않습니다.'})"""

def signout(request):   #로그아웃 기능
    return render(request, 'login/user.html')

def find_id(request):
    return render(request, 'login/find_id.html')

def find_pw(request):
    return render(request, 'login/find_pw.html')