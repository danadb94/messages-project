from django.contrib import admin
from core.models import Message


@admin.register(Message)
class Messageadmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'subject', 'message', 'creation_date', 'read_message', )
    autocomplete_fields = ('receiver', )
