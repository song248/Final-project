from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank = True, null=True)

    def __str__(self):
        return self.title   

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def hide(self):
        self.published_date = None
        self.save()
