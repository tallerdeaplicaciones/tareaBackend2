from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User

# Create your models here.    
class Tech(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'
    
class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tech = models.ForeignKey(Tech, null=True,blank = True, on_delete=models.RESTRICT)
    def __str__(self) -> str:
        return self.title