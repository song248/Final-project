from django.shortcuts import render
from django.views.generic import View, CreateView, TemplateView
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout


#from .forms import UserForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

#-------------------------------------------------------------------------------------------------------
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

class UserLoginView(LoginView):           # 로그인
    template_name = 'login/login_2.html'

    # def form_invalid(self, form):
    #     messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
    #     return super().form_invalid(form)   
#-------------------------------------------------------------------------------------------------------

class LoginSuccess(CreateView):
    template_name = 'login/main.html'

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


def main(request):
    return render(request, 'login/main.html')

def signout(request):   #로그아웃 기능
    return render(request, 'login/user.html')

def find_id(request):
    return render(request, 'login/find_id.html')

def find_pw(request):
    return render(request, 'login/find_pw.html')

#-------------------------------------------------------------------------------------------------------


def signup(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))

    context = {'form': form}
    return render(request, 'simp_web/signup.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/simp_web')
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'simp_web/login.html', {'form': form})
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return HttpResponseRedirect('/simp_web')
            else:
                print('User not found')
        else:
            # If there were errors, we render the form with these
            # errors
            return render(request, 'simp_web/login.html', {'form': form})