from core.models import Message, UserMessage
from core.serializers import MessageSerializer, UserMessageSerializer
from django.db.models import Q
from rest_framework import mixins, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action


class MessageView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):

    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))\
            .order_by("-creation_date").distinct()

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

        # User send to himself, delete the whole message and delete relevant rows from UserMessage
        if user == sender and [user.email] == receivers:
            self.perform_destroy(instance)
            UserMessage.objects.filter(Q(user=user) & Q(message=instance)).delete()

        # User is receiver/ sender or both (but includes additional receivers),delete relevant rows from UserMessage
        else:
            UserMessage.objects.filter(Q(user=user) & Q(message=instance)).delete()

        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMessageView(generics.RetrieveAPIView, mixins.ListModelMixin, GenericViewSet):

    serializer_class = UserMessageSerializer
    permission_classes = (IsAuthenticated,)
    queryset = UserMessage.objects.all()

    # Get messages of only logged-in user, newest messages first.
    def get_queryset(self):
        user = self.request.user
        return UserMessage.objects.filter(user=user).order_by("-creation_date").distinct()

    # read message
    def retrieve(self, request, *args, **kwargs):

        # get message id and find it in UserMessage. user can read messages he received.
        msg_id = self.request.parser_context['kwargs']['pk']
        query = UserMessage.objects.values_list('id').filter(message=msg_id, user=self.request.user, sender=False)

        if query:
            # get read message id and update read field to True
            read_message_id = query[0][0]
            read_msg_obj = UserMessage.objects.get(pk=read_message_id)
            read_msg_obj.read = True
            read_msg_obj.save()

            serializer = UserMessageSerializer(read_msg_obj)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False)
    def unread_messages(self, pk=None):
        # Get all unread messages of only logged-in user, messages that the user sent will not be included.
        queryset = UserMessage.objects.filter(Q(user=self.request.user) & Q(read=False) & Q(sender=False))\
            .order_by("-creation_date")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


