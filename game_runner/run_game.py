import sys
import time

from game_runner.server import server_runner
from game_runner.client import client_runner


def run_game(client1_name, client1_path, client1_language,
             client2_name, client2_path, client2_language):
    server_runner.start(client1_name, client2_name)
    print('WAITING FOR SERVER')
    time.sleep(8)
    print('RUNNING CLIENTS')

    language_runners = {
        'PYTHON': client_runner.run_client_python,
        'JAVA': client_runner.run_client_java,
        'CPP': client_runner.run_client_cpp,
    }
    if client1_language not in language_runners:
        raise ValueError('Client 1 language not in options: PYTHON, JAVA, CPP')
    if client2_language not in language_runners:
        raise ValueError('Client 2 language not in options: PYTHON, JAVA, CPP')
    client1_process = language_runners[client1_language](client1_path)
    client2_process = language_runners[client2_language](client2_path)
