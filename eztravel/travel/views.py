from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.
# def index(request):
#     return HttpResponse("Hello world")

def index(request):
    return render(request, 'travel/index.html')

# def know(request):
#     return render(request, 'travel/know.html')

def know(request):
    # postlist = Post.objects.all()
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


