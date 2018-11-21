import os
import re
import sys
import time
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_runner.server import server_runner
from game_runner.client import client_runner


def run_game(game_id, team1_name, team1_language, team1_path, team2_name, team2_language, team2_path, callback_url):
    print(game_id, team1_name, team1_language, team1_path, team2_name, team2_language, team2_path, callback_url)
    server_runner.start(game_id=game_id, team1_name=team1_name, team2_name=team2_name, callback_url=callback_url)
    print('WAITING FOR SERVER')
    time.sleep(8)
    print('RUNNING CLIENTS')

    language_runners = {
        'PYTHON': client_runner.run_client_python,
        'JAVA': client_runner.run_client_java,
        'CPP': client_runner.run_client_cpp,
    }

    client1_process = language_runners[team1_language](team1_path)
    client2_process = language_runners[team2_language](team2_path)


def return_results(game_id, callback_url):
    log_path = os.path.join(server_runner.SERVER_DIR_PATH, str(game_id) + '.log')
    with open(log_path, 'r') as lf:
        log = lf.read()
        results = re.findall(r'END\n([^\n]*)', log)[0].split(':')
        results_team1 = results[0].split()
        results_team2 = results[1].split()
    data = {'game_id': game_id,
            'team1_name': results_team1[0], 'team1_goals': results_team1[1],
            'team2_name': results_team2[1], 'team2_goals': results_team2[0]}
    files = {'log_file': open(log_path, 'rb')}
    print('RETURNING TO MAIN SERVER: {}, {} {}:{} {}'.format(
        callback_url, results_team1[0], results_team1[1], results_team2[0], results_team2[1],
    ))
    r = requests.post(callback_url, data=data, files=files)
    print('{}: {}'.format(r.status_code, r.content))


if __name__ == '__main__':
    run_game(
        game_id=sys.argv[1],
        team1_name=sys.argv[2],
        team1_language=sys.argv[3].upper(),
        team1_path=sys.argv[4],
        team2_name=sys.argv[5],
        team2_language=sys.argv[6].upper(),
        team2_path=sys.argv[7],
        callback_url=sys.argv[8] if len(sys.argv) >= 8 else None,
    )
