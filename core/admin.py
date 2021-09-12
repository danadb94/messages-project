from django.contrib import admin
from core.models import Message,UserMessage


@admin.register(Message)
class Messageadmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'subject', 'message', 'creation_date', )
    autocomplete_fields = ('receiver', )


@admin.register(UserMessage)
class UserMessageadmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'read', 'sender', )