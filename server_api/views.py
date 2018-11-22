import os
import zipfile
import subprocess
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import *

from server_api.models import Game
from uiai2018_game_runner_server.settings import BASE_DIR


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
    codes_dir = os.path.join(BASE_DIR, 'codes', str(game.pk))
    with zipfile.ZipFile(game.team1_code.path, "r") as zip_ref:
        zip_ref.extractall(os.path.join(codes_dir, 'team1'))
    with zipfile.ZipFile(game.team2_code.path, "r") as zip_ref:
        zip_ref.extractall(os.path.join(codes_dir, 'team2'))
    run_in_lxc = request.data.get('run_in_lxc', True)
    if run_in_lxc:
        subprocess.run(['./run-lxc.sh', str(game.game_id), game.team1_name, game.team1_language,
                        os.path.join(codes_dir, 'team1'), game.team2_name, game.team2_language,
                        os.path.join(codes_dir, 'team2')], cwd=BASE_DIR)
    else:
        subprocess.Popen(
            ['python3', 'run_game.py', str(game.game_id), game.team1_name, game.team1_language,
             os.path.join(codes_dir, 'team1'), game.team2_name, game.team2_language, os.path.join(codes_dir, 'team2'),
             request.data['callback_url']],
            cwd=os.path.join(BASE_DIR, 'game_runner')
        )
    return Response({'message': 'Game added to queue'}, HTTP_201_CREATED)
