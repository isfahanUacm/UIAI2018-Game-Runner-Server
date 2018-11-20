import os
import glob
import subprocess


def run_client_python(client_dir_path):
    cmd_run = subprocess.Popen(['python3', 'Game.py'], cwd=client_dir_path)
    return cmd_run


def run_client_java(client_dir_path):
    client_files = glob.glob(os.path.join(client_dir_path, '*.java'))
    cmd_clean = subprocess.run(['rm', '-r', 'out'], cwd=client_dir_path)
    cmd_mkdir = subprocess.run(['mkdir', 'out'], cwd=client_dir_path)
    cmd_compile = subprocess.run(['javac'] + client_files + ['-d', 'out'], cwd=client_dir_path)
    cmd_run = subprocess.Popen(['java', 'Main'], cwd=os.path.join(client_dir_path, 'out'))
    return cmd_run


def run_client_cpp(client_dir_path):
    client_files = glob.glob(os.path.join(client_dir_path, '*.cpp'))
    cmd_clean = subprocess.run(['rm', 'out'], cwd=client_dir_path)
    cmd_compile = subprocess.run(['g++'] + client_files + ['-o', 'out'], cwd=client_dir_path)
    cmd_run = subprocess.Popen(['./out'], cwd=client_dir_path)
    return cmd_run
