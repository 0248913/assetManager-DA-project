from django.db import models
from django.utils import timezone

import random
import string
from django.contrib.auth.models import User
from django.db import models

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey('Space', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    information = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Meta:
    permissons = [
        ("delete_log", "Can delete log")
        ]


class Space(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_spaces')
    members = models.ManyToManyField(User, related_name='spaces')
    name = models.CharField(max_length=100)
    descriptions = models.TextField()
    code = models.CharField(max_length=8, unique=True, null=True)

    def generateCode(self):
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(8))
        while Space.objects.filter(code=code).exists():
            code = ''.join(random.choice(characters) for _ in range(8))
        return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generateCode()
        super().save(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
class spaceRoles(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('member', 'Member'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'space')