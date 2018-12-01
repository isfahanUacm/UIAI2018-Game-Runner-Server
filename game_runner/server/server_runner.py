import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVER_DIR_PATH = os.path.join(BASE_DIR, 'server_linux_x86_64')
SERVER_FILE_NAME = 'UIAI2018Server_Linux_x86_64_3.0.x86_64'


def start(game_id, team1_name, team2_name):
    # --mode=cvc --logfile=log_file_name.log --speed=20 --team1name=chom --team2name=choooom -nographics -batchmode
    command = ['./{}'.format(SERVER_FILE_NAME),
               '--mode=cvc', '--logfile={}.log'.format(str(game_id)), '--speed=20',
               '--team1name={}'.format(team1_name), '--team2name={}'.format(team2_name)]
    process = subprocess.Popen(command, cwd=SERVER_DIR_PATH)
    return process
