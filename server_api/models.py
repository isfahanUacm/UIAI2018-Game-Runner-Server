import os
from django.db import models

from uiai2018_game_runner_server.settings import BASE_DIR


class Game(models.Model):
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    ERROR = 'ERROR'
    ENDED = 'ENDED'
    STATUS_OPTIONS = (WAITING, RUNNING, ERROR, ENDED)

    PYTHON, JAVA, CPP = 'PYTHON', 'JAVA', 'CPP'
    LANGUAGES = (PYTHON, JAVA, CPP)

    game_id = models.IntegerField()
    team1_name = models.CharField(max_length=32)
    team1_code = models.FileField(upload_to='codes')
    team1_language = models.CharField(max_length=8, choices=((l, l) for l in LANGUAGES))
    team2_name = models.CharField(max_length=32)
    team2_code = models.FileField(upload_to='codes')
    team2_language = models.CharField(max_length=8, choices=((l, l) for l in LANGUAGES))
    status = models.CharField(max_length=8, choices=((s, s) for s in STATUS_OPTIONS), default=WAITING)
    date_added = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=64)

    def __str__(self):
        return '{} vs {}; @{}'.format(self.team1_name, self.team2_name, self.date_added)

    def get_team1_code_path(self):
        return os.path.join(BASE_DIR, 'codes', str(self.pk), 'team1')

    def get_team2_code_path(self):
        return os.path.join(BASE_DIR, 'codes', str(self.pk), 'team2')
