from django.contrib import admin
from .models import CustomUser 

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'auth_type', 'is_verified')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email', 'auth_type', 'is_verified')
    

