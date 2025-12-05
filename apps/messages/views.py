from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class CreateChatView(APIView):
    """
    Create a chat.
    - For DM, pass 1 user in participants
    - For group chat, set is_group=True & pass multiple participants
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        participants = data.get("participants", [])

        if request.user.id not in participants:
            participants.append(request.user.id)

        is_group = data.get("is_group", False)

        if not is_group and len(participants) != 2:
            return Response({"error": "DM chat must have exactly 2 participants."})

        chat = Chat.objects.create(
            name=data.get("name", "") if is_group else "", is_group=is_group
        )
        chat.participants.set(participants)
        chat.save()

        return Response(ChatSerializer(chat).data, status=201)


class ListChatsView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user).order_by(
            "-created_at"
        )


class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        if request.user not in chat.participants.all():
            return Response({"error": "Not allowed."}, status=403)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, chat=chat)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChatMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs["chat_id"]
        chat = Chat.objects.get(id=chat_id)

        if self.request.user not in chat.participants.all():
            return Message.objects.none()

        return chat.messages.all()


class MarkSeenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, message_id):
        msg = Message.objects.get(id=message_id)

        if request.user not in msg.chat.participants.all():
            return Response({"error": "Not allowed."}, status=403)

        msg.is_seen = True
        msg.seen_at = timezone.now()
        msg.save()

        return Response({"status": "seen"})
