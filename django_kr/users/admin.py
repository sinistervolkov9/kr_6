from django.contrib import admin
from .models import User


@admin.register(User)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'country',)
    list_filter = ('username',)
