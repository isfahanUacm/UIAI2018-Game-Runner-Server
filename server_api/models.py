from django.db import models


class Game(models.Model):
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    ERROR = 'ERROR'
    ENDED = 'ENDED'
    STATUS_OPTIONS = (WAITING, RUNNING, ERROR, ENDED)

    PYTHON, JAVA, CPP = 'PYTHON', 'JAVA', 'CPP'
    LANGUAGES = (PYTHON, JAVA, CPP)

    team1_name = models.CharField(max_length=32)
    team1_code = models.FileField(upload_to='codes')
    team1_language = models.CharField(max_length=8, choices=((l, l) for l in LANGUAGES))
    team2_name = models.CharField(max_length=32)
    team2_code = models.FileField(upload_to='codes')
    team2_language = models.CharField(max_length=8, choices=((l, l) for l in LANGUAGES))
    log_file = models.FileField(upload_to='logs', blank=True, null=True)
    status = models.CharField(max_length=8, choices=((s, s) for s in STATUS_OPTIONS), default=WAITING)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} vs {}; @{}'.format(self.team1_name, self.team2_name, self.date_added)
