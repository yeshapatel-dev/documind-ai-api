from django.urls import path

from apps.documents.api.v1.views.chat_view import ChatAPIView


urlpatterns = [
    # chat API
    path(
        "chat/",ChatAPIView.as_view(), name="chat",
    ),
]