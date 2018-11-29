import glob
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

    def __str__(self):
        return 'GAME{}: {} vs {}'.format(self.game_id, self.team1_name, self.team2_name)

    def get_team1_code_path(self):
        return os.path.join(BASE_DIR, 'codes', str(self.game_id), 'team1')

    def get_team2_code_path(self):
        return os.path.join(BASE_DIR, 'codes', str(self.game_id), 'team2')

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


class CompileRequest(models.Model):
    PYTHON, JAVA, CPP = 'PYTHON', 'JAVA', 'CPP'
    LANGUAGE_OPTIONS = (PYTHON, JAVA, CPP)

    WAITING = 'WAITING'
    COMPILING = 'COMPILING'
    COMPILATION_OK = 'COMPILATION_OK'
    COMPILATION_ERROR = 'COMPILATION_ERROR'
    STATUS_OPTIONS = (WAITING, COMPILING, COMPILATION_OK, COMPILATION_ERROR)

    code_id = models.IntegerField(primary_key=True)
    compilation_status = models.CharField(max_length=18, choices=((s, s) for s in STATUS_OPTIONS), default=WAITING)
    compile_status_text = models.TextField(max_length=8192, blank=True, null=True)
    code_zip = models.FileField(upload_to=os.path.join('temp', 'compile'))
    language = models.CharField(max_length=6, choices=((l, l) for l in LANGUAGE_OPTIONS))
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_extraction_path(self):
        return os.path.join(BASE_DIR, 'temp', 'compile', str(self.pk))

    def extract(self):
        os.mkdir(self.get_extraction_path())
        with zipfile.ZipFile(self.code_zip.path, "r") as z:
            z.extractall(self.get_extraction_path())

    def compile(self):
        self.extract()
        if self.language == CompileRequest.PYTHON:
            self.compile_status_text = 'بدون نیاز به کامپایل'
            self.compilation_status = CompileRequest.COMPILATION_OK
            self.save()
        elif self.language == CompileRequest.JAVA:
            self.compilation_status = CompileRequest.COMPILING
            self.save()
            client_files = glob.glob(os.path.join(self.get_extraction_path(), '*.java'))
            subprocess.run(['rm', '-r', 'out'], cwd=self.get_extraction_path())
            subprocess.run(['mkdir', 'out'], cwd=self.get_extraction_path())
            p = subprocess.run(['javac'] + client_files + ['-d', 'out'], cwd=self.get_extraction_path(),
                               stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            if p.returncode == 0:
                self.compilation_status = CompileRequest.COMPILATION_OK
                self.compile_status_text = 'کد جاوا شما با موفقیت کامپایل شد.'
                self.save()
            else:
                self.compilation_status = CompileRequest.COMPILATION_ERROR
                self.compile_status_text = p.stdout.decode("utf-8")
                self.save()
        elif self.language == CompileRequest.CPP:
            client_files = glob.glob(os.path.join(self.get_extraction_path(), '*.cpp'))
            subprocess.run(['rm', 'out'], cwd=self.get_extraction_path())
            p = subprocess.run(['g++', '-std=gnu++11'] + client_files + ['-o', 'out'], cwd=self.get_extraction_path(),
                               stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            if p.returncode == 0:
                self.compilation_status = CompileRequest.COMPILATION_OK
                self.compile_status_text = 'کد ++C شما با موفقیت کامپایل شد.'
                self.save()
            else:
                self.compilation_status = CompileRequest.COMPILATION_ERROR
                self.compile_status_text = p.stdout.decode("utf-8")
                self.save()
        subprocess.run(['rm', '-r', self.get_extraction_path()])
        return self.compilation_status

    def get_callback_dict(self):
        return {
            'id': self.code_id,
            'status': self.compilation_status,
            'message': self.compile_status_text,
        }
