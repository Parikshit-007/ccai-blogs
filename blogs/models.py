from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='static/images/')
    date = models.DateTimeField(null=False)

    def __str__(self):
        return self.title
    @classmethod
    def search(cls, query):
        # Perform case-insensitive search on title and content fields
        return cls.objects.filter(models.Q(title__icontains=query) | models.Q(content__icontains=query)).order_by('-date')

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name
