import subprocess
import os

booyah_root = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
booyah_parent_src = os.path.realpath(os.path.abspath(os.path.join(booyah_root, '..')))

class BooyahServer:

    @classmethod
    def run(cls):
        """
        Check if pip installed and install requirements.txt
        enter the src dir of current folder
        start gunicorn application server
        """
        if subprocess.run(["command", "-v", "pip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            pip_command = "pip"
        else:
            pip_command = "pip3"
        os.chdir(booyah_parent_src)
        subprocess.run([pip_command, "install", "-r", "requirements.txt"])
        os.chdir(os.getcwd())
        subprocess.run(["gunicorn", "application"])