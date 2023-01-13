from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(CustomUser):
    list_display = ('username', 'email',
                    'first_name', 'last_name', 'role')
