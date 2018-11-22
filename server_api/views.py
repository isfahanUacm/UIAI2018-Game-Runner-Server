from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import *

from server_api.models import Game


@api_view(['GET'])
def get_server_status(request):
    return Response({'status': 'READY', 'code': 200}, status=HTTP_200_OK)


@api_view(['POST'])
def request_game(request):
    game = Game(
        game_id=int(request.data['game_id']),
        team1_name=request.data['team1_name'],
        team1_language=request.data['team1_language'].upper(),
        team1_code=request.data['team1_code'],
        team2_name=request.data['team2_name'],
        team2_language=request.data['team2_language'].upper(),
        team2_code=request.data['team2_code'],
    )
    game.save()
    game.run()
    return Response({'message': 'Game added to queue'}, HTTP_201_CREATED)
