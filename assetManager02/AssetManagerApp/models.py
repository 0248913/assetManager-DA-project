from django.db import models
from django.utils import timezone
import random
import string
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey('Space', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    information = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    in_use = models.BooleanField(default=False)
    last_changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_changed_logs')
    

    class Meta:
        permissions = [
            ("delete_log", "Can delete log"),
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
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
   
        if self.role == 'owner':
            self.assign_owner_permissions()
        elif self.role == 'member':
            self.assign_member_permissions()

    def assign_owner_permissions(self):
        
        content_type = ContentType.objects.get_for_model(UserLog)

  
        owner_permissions = Permission.objects.filter(content_type=content_type).filter(
            codename__in=['delete_log', 'can_edit_logs', 'can_delete_logs'])
        self.user.user_permissions.add(*owner_permissions)

    def assign_member_permissions(self):
      
        content_type = ContentType.objects.get_for_model(UserLog)

     
        member_permissions = Permission.objects.filter(content_type=content_type).filter(
            codename__in=['can_edit_logs'])
        self.user.user_permissions.add(*member_permissions)

    class Meta:
        permissions = [
            ('can_edit_logs', 'Can edit logs'),
            ('can_delete_logs', 'Can delete logs'),
        ]
