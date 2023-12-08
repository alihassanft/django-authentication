from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)

class User(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name','username', 'email')