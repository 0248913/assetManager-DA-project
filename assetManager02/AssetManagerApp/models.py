from turtle import title
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import related
from django.db.models import CASCADE


class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey('Space', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    information = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Space(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_spaces')
    name = models.CharField(max_length=100)
    descriptions = models.TextField()
    
class SpaceMemberManagment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   space = models.ForeignKey(Space, on_delete=models.CASCADE)
