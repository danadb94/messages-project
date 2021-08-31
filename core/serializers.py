from core.models import Message
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', ]


# iterate over all receivers, make sure which are not existing in the database to create them.
def new_receivers(receivers_email):
    existing_email = User.objects.filter(email__in=receivers_email)

    new_receivers_email = list(receivers_email)
    if existing_email:
        for receiver in existing_email:
            new_receivers_email.remove(receiver.email)

    for receiver in range(len(new_receivers_email)):
        user = new_receivers_email[receiver]
        new_receivers_email[receiver] = User(username=user, email=user)

    return new_receivers_email


class MessageSerializer(serializers.ModelSerializer):
    # Display and create object by using receiver email instead of user pk
    receiver = UserSerializer(many=True, read_only=False)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'subject', 'message', 'creation_date', 'read_message', ]
        read_only_fields = ('sender', 'creation_date', 'read_message', )

    def create(self, validated_data):
        receivers = validated_data.pop('receiver')

        receivers_email = []
        for receiver in receivers:
            receivers_email.append(receiver['email'])

        # create new receivers
        new_receivers_email = new_receivers(receivers_email)
        User.objects.bulk_create(new_receivers_email)

        message = Message.objects.create(**validated_data)

        # relate receivers to message
        receivers = User.objects.filter(email__in=receivers_email)
        for receiver in receivers:
            message.receiver.add(receiver.id)

        message.save()
        return message


