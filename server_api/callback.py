import os
import re

import pyinotify
import requests

from uiai2018_game_runner_server.settings import BASE_DIR

CALLBACK_URL = 'http://acm.ui.ac.ir/uiai2018/games/callback/'

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE


class GameCallbackHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event):
        log_path = event.pathname
        game_id = re.findall(r'(\d+).log', log_path)[0]
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
            CALLBACK_URL, results_team1[0], results_team1[1], results_team2[0], results_team2[1],
        ))
        requests.post(CALLBACK_URL, data=data, files=files)


handler = GameCallbackHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(os.path.join(BASE_DIR, 'logs'), mask, rec=True)
notifier.loop()
