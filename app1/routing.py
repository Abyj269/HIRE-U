from django.urls import path
from .import consumers

websocket_urlpatterns=[
    path('chatbox/<int:id>/',consumers.ChatConsumer.as_asgi()),
    path('jobseekerchatbox/<int:id>/',consumers.ChatConsumer.as_asgi()),
]