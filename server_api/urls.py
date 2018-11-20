from django.urls import path

from server_api.views import *

urlpatterns = [
    path('game/request/', request_game, name='request_game'),
    path('server/status/', get_server_status, name='get_server_status'),
]
