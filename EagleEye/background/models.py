from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password')

admin.site.register(User,UserAdmin)