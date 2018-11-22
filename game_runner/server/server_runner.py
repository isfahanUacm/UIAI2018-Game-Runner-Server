import os
import threading
import subprocess

from game_runner.run_game import return_results

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVER_DIR_PATH = os.path.join(BASE_DIR, 'server_linux_x86_64')
SERVER_FILE_NAME = 'UIAIServer2018_1.1.x86_64'


def start(game_id, team1_name, team2_name):
    # --mode=cvc --logfile=log_file_name.log --speed=20 --team1name=chom --team2name=choooom -nographics -batchmode
    command = ['./{}'.format(SERVER_FILE_NAME),
               '--mode=cvc', '--logfile={}.log'.format(str(game_id)), '--speed=100', '-nographics', '-batchmode',
               '--team1name={}'.format(team1_name), '--team2name={}'.format(team2_name)]
    process = subprocess.Popen(command, cwd=SERVER_DIR_PATH)
    return process
