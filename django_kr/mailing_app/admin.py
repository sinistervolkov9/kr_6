from django.contrib import admin
from .models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment', 'user',)
    list_filter = ('user',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',)
    list_filter = ('user',)


@admin.register(Mailing)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'periodicity',)
    list_filter = ('id',)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_time', 'status')
    list_filter = ('attempt_time',)
