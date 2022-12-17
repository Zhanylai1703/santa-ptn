from django.contrib.auth.models import AbstractUser
from django.db import models


class Owner(AbstractUser):
    owned_groups = models.ManyToManyField('Group')
    # description = models.TextField(blank=True)
    # finish = models.DateTimeField(auto_now_add=True)
    # finish_registration = models.DateTimeField(auto_now=True)



class SimpleUser(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    answers = models.ForeignKey('FieldAnswer', blank=True, null=True, on_delete=models.CASCADE)
    assigned = models.ForeignKey('SimpleUser', blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name





class Group(models.Model):
    name = models.CharField(max_length=150)
    fields = models.ManyToManyField('Field')
    # description = models.TextField(blank=True)
    # finish = models.DateTimeField(auto_now_add=True)
    # finish_registration = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Field(models.Model):
    name = models.CharField(max_length=150)
    is_required = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class FieldAnswer(models.Model):
    answer = models.CharField(max_length=600)
    field = models.ManyToManyField('Field')
    user = models.ManyToManyField('SimpleUser')

    def __str__(self):
        return self.answer