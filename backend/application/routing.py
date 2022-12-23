# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path, re_path
from application.websocketConfig import MegCenter,realTimeChatConsumer


websocket_urlpatterns = [
    path('ws/<str:service_uid>/', MegCenter.as_asgi()), #consumers.DvadminWebSocket 是该路由的消费者
    # path('asr/<str:room_name>/',realTimeChatConsumer.as_asgi()),
    re_path(r'^ws/asr/(?P<room_name>\w+)/$',realTimeChatConsumer.as_asgi())
]

