from core.models import Message
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    # Display and create object by using receiver email instead of user pk
    receiver = SlugRelatedField(slug_field="email", queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'subject', 'message', 'creation_date', 'read_message', ]
        read_only_fields = ('sender', 'creation_date', 'read_message', )

    # Display sender email instead of user pk
    def to_representation(self, instance):
        data = super(MessageSerializer, self).to_representation(instance)
        data['sender'] = instance.sender.email
        return data


