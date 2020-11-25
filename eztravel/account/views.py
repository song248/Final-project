from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

# Create your views here.
class userLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = ''
    
class userRegister(CreateView):
    template_name = 'account/signup.html'
    form_class = UserCreationForm
    success_url = '/login/complete/'

class registComplete(View):
    def get(self, request):
        return render(request, 'account/complete.html')

def test(request):
    return render(request, 'travel/index.html')

