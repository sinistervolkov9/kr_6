from django.contrib import admin
from .models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment', 'user', )
    list_filter = ('user', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', )
    list_filter = ('user', )


@admin.register(Mailing)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'periodicity', )
    list_filter = ('user', )

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    pass
