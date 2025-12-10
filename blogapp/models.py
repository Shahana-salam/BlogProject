
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_pic= models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username if self.user else "No User"



class Category(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return '{}'.format(self.name)



class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)


def __str__(self):
        return '{}'.format(self.title)



class Comment(models.Model):
    post = models.ForeignKey("Posts", related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_owner(self, user):
        return self.user == user

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

