from core.models import Message, ReadMessage
from core.serializers import MessageSerializer, ReadMessageSerializer
from django.db.models import Q
from rest_framework import mixins, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User


class MessageView(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                  mixins.ListModelMixin, generics.RetrieveAPIView, GenericViewSet):

    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    # Get messages of only logged-in user, newest messages first.
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))\
            .order_by("-creation_date").distinct()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    # Delete selected message only from the logged-in user and not thw whole message
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        user = self.request.user
        sender = instance.sender
        receivers_data = instance.receiver
        # get only receivers emails
        receivers = []
        for receiver in receivers_data.all():
            receivers.append(receiver.email)

        # User send to himself, delete the whole message
        if user == sender and [user.email] == receivers:
            self.perform_destroy(instance)
        # Delete sender from the message
        elif user == sender and user.email not in receivers:
            instance.sender = None
            instance.save()

        # User is receiver
        else:
            # Delete record of receiver-message from ReadMessage for not displaying him it
            msg_id = self.request.parser_context['kwargs']['pk']
            read_msg_obj = ReadMessage.objects.get(message=msg_id, receiver=user)
            read_msg_obj.delete()

            # Delete receiver from the message
            receivers.remove(user.email)

            # Get a list of ids of updated receivers and set them in the message.
            updated_receivers = User.objects.values_list('id').filter(email__in=receivers)
            updated_data = []
            if updated_receivers:
                for receiver in updated_receivers:
                    updated_data.append(receiver[0])

            instance.receiver.set(updated_data)
            # user is also a sender
            if user == sender:
                instance.sender = None

            instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReadMessageView(generics.RetrieveAPIView, mixins.ListModelMixin, GenericViewSet):

    serializer_class = ReadMessageSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ReadMessage.objects.all()

    # unread message
    def list(self, request, *args, **kwargs):
        # Get all unread messages of only logged-in user, messages that the user sent will not be included.
        queryset = ReadMessage.objects.filter(Q(receiver=self.request.user) & Q(read=False))\
            .order_by("-creation_date")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # read message
    def retrieve(self, request, *args, **kwargs):

        # get message id and find it in ReadMessage
        msg_id = self.request.parser_context['kwargs']['pk']
        query = ReadMessage.objects.values_list('id').filter(message=msg_id, receiver=self.request.user)

        if query:
            # get read message id and update read field to True
            read_message_id = query[0][0]
            read_msg_obj = ReadMessage.objects.get(pk=read_message_id)
            read_msg_obj.read = True
            read_msg_obj.save()

            serializer = ReadMessageSerializer(read_msg_obj)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)



