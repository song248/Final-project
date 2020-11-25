from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from .models import Post

# Create your views here.
class mainview(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        context = {
            'user': request.user.username,
            'default': True,
        }
        return render(request, 'travel/index.html', context)

def index(request):
    return render(request, 'travel/index.html')

def know(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')
    context = {
        'posts': posts,
    } 
    return render(request, 'travel/know.html', context)

def know_show(request, pk):
    post = Post.objects.get(pk=pk)
    context={
        'post':post
    }
    return render(request, 'travel/know_show.html', context)

def howto(request):
    return render(request, 'travel/howto.html')

def login(request):
    return render(request, 'travel/login.html')

def upload(request):
    return render(request, 'travel/map.html')

def loading(request):
    return render(request, 'travel/loading.html')

class PostTemplateView(TemplateView):
    template_name = 'travel/loading.html'

# def post_json(request):
#     data = list(Post.objects.values())
#     return JsonResponse(data, safe=False)