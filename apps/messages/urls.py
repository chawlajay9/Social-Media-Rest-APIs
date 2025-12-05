from django.urls import path
from .views import (
    CreateChatView,
    ListChatsView,
    SendMessageView,
    ChatMessagesView,
    MarkSeenView,
)

urlpatterns = [
    path("create/", CreateChatView.as_view()),
    path("list/", ListChatsView.as_view()),
    path("<int:chat_id>/send/", SendMessageView.as_view()),
    path("<int:chat_id>/messages/", ChatMessagesView.as_view()),
    path("seen/<int:message_id>/", MarkSeenView.as_view()),
]
