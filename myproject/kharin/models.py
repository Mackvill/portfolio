from django.db import models
from django.contrib.auth.models import AbstractUser , Group, Permission
from django.utils.translation import gettext_lazy as _
class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')


    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True,
                                              related_name='customuser_permissions')

    def __str__(self):
        return self.username

class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class PhotoSessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.IntegerField()
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Session {self.session_id} - {self.client.name} "

class CompletedSessions(models.Model):
    completion_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(PhotoSessions, on_delete=models.CASCADE)
    photographer_name = models.CharField(max_length=100)
    completed_date = models.DateField()

    def __str__(self):
        return f"Completion {self.completion_id}"

