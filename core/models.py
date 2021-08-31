from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ManyToManyField(User, null=True, related_name="receiver")
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    read_message = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.email}- {self.subject}'
