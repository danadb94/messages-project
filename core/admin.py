from django.contrib import admin
from core.models import Message,ReadMessage


@admin.register(Message)
class Messageadmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'subject', 'message', 'creation_date', )
    autocomplete_fields = ('receiver', )


@admin.register(ReadMessage)
class ReadMessageadmin(admin.ModelAdmin):
    list_display = ('id', 'receiver', 'message', 'read', )

