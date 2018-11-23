import os
import re
import time
import requests
import pyinotify

from django.core.management import BaseCommand
from uiai2018_game_runner_server.settings import BASE_DIR

CALLBACK_URL = 'http://acm.ui.ac.ir/uiai2018/games/callback/'


class GameCallbackHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event):
        game_id = None
        try:
            log_path = event.pathname
            print('LOG DETECTED: {}'.format(log_path))
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
            response = requests.post(CALLBACK_URL, data=data, files=files)
            print('GAME{}: {}'.format(game_id, response.status_code))
        except BaseException as e:
            output_path = os.path.join(BASE_DIR, 'error-{}.txt'.format(game_id if game_id else int(time.time())))
            with open(output_path, 'w+') as f:
                f.write(str(e))


class Command(BaseCommand):

    def handle(self, *args, **options):
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_CREATE

        handler = GameCallbackHandler()
        notifier = pyinotify.Notifier(wm, handler)
        wdd = wm.add_watch(os.path.join(BASE_DIR, 'logs'), mask, rec=True)
        notifier.loop()
