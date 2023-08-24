import subprocess
import os

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
        subprocess.run([pip_command, "install", "-r", "requirements.txt"])
        subprocess.run(["gunicorn", "application"])