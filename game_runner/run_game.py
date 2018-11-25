import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_runner.server import server_runner
from game_runner.client import client_runner


def run_game(game_id, team1_name, team1_language, team1_path, team2_name, team2_language, team2_path):
    print('WAITING FOR SERVER')
    server_process = server_runner.start(game_id=game_id, team1_name=team1_name, team2_name=team2_name)
    time.sleep(8)
    print('RUNNING CLIENTS')

    language_runners = {
        'PYTHON': client_runner.run_client_python,
        'JAVA': client_runner.run_client_java,
        'CPP': client_runner.run_client_cpp,
    }

    client1_process = language_runners[team1_language](team1_path)
    client2_process = language_runners[team2_language](team2_path)

    server_process.wait()


if __name__ == '__main__':
    run_game(
        game_id=sys.argv[1],
        team1_name=sys.argv[2],
        team1_language=sys.argv[3].upper(),
        team1_path=sys.argv[4],
        team2_name=sys.argv[5],
        team2_language=sys.argv[6].upper(),
        team2_path=sys.argv[7],
    )
