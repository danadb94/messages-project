from core.models import Message
from core.serializers import MessageSerializer
from django.db.models import Q
from rest_framework import mixins, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action


class MessageView(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                  mixins.ListModelMixin, generics.RetrieveAPIView, GenericViewSet):

    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    # Get messages of only logged-in user, newest messages first.
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))\
            .order_by("-creation_date")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()

        # update read message field
        message.read_message = True
        message.save()

        serializer = self.get_serializer(message)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, )
    def unread_messages(self, pk=None):

        # Get all unread messages of only logged-in user, messages that the user sent will not be included.
        query = Message.objects.filter(Q(receiver=self.request.user) & Q(read_message=False))\
            .order_by("-creation_date")

        serializer = MessageSerializer(query, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
