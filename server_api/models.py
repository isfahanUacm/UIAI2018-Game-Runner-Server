import os
import zipfile
import subprocess

from django.db import models

from uiai2018_game_runner_server.settings import BASE_DIR


class Game(models.Model):
    PYTHON, JAVA, CPP = 'PYTHON', 'JAVA', 'CPP'
    LANGUAGES = (PYTHON, JAVA, CPP)

    game_id = models.IntegerField(primary_key=True)
    team1_name = models.CharField(max_length=32)
    team1_code = models.FileField(upload_to='codes')
    team1_language = models.CharField(max_length=8, choices=((l, l) for l in LANGUAGES))
    team2_name = models.CharField(max_length=32)
    team2_code = models.FileField(upload_to='codes')
    team2_language = models.CharField(max_length=8, choices=((l, l) for l in LANGUAGES))
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} vs {}; @{}'.format(self.team1_name, self.team2_name, self.date_added)

    def get_team1_code_path(self):
        return os.path.join(BASE_DIR, 'codes', str(self.pk), 'team1')

    def get_team2_code_path(self):
        return os.path.join(BASE_DIR, 'codes', str(self.pk), 'team2')

    def run(self, run_in_lxc=True):
        print('RUNNING GAME{}: {} vs {}'.format(self.game_id, self.team1_name, self.team2_name))
        codes_dir = os.path.join(BASE_DIR, 'codes', str(self.game_id))
        with zipfile.ZipFile(self.team1_code.path, "r") as zip_ref:
            zip_ref.extractall(os.path.join(codes_dir, 'team1'))
        with zipfile.ZipFile(self.team2_code.path, "r") as zip_ref:
            zip_ref.extractall(os.path.join(codes_dir, 'team2'))
        cmd = ['./run-lxc.sh'] if run_in_lxc else ['python3', 'run_game.py']
        cmd += [str(self.game_id),
                self.team1_name, self.team1_language, os.path.join(codes_dir, 'team1'),
                self.team2_name, self.team2_language, os.path.join(codes_dir, 'team2')]
        subprocess.Popen(cmd, cwd=os.path.join(BASE_DIR, 'game_runner'))
