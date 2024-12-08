# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone





class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)
  def __str__(self):
          return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="email address")
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    favorite_categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.username   
class Article(models.Model):
    newsapi_id = models.CharField(max_length=200, unique=True, null=True)  # Unique identifier from NEWSAPI
    title = models.CharField(max_length=200)  # You might still store the title for easy reference
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', null=True)

    def __str__(self):
        return self.title



class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


    def __str__(self):
        return f'Comment by {self.author} on {self.article}'


