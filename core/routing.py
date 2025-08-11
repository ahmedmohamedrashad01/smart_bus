from django.urls import path
from .consumers import BusLiveConsumer

websocket_urlpatterns = [
    path('ws/buses/<int:bus_id>/live/', BusLiveConsumer.as_asgi()),
]
