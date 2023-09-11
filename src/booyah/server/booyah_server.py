import subprocess
import os
from py_dotenv import read_dotenv
read_dotenv('.env')

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
        booyah_env = os.getenv('BOOYAH_ENV')
        if booyah_env and booyah_env.lower() == 'production':
            subprocess.run(["gunicorn", "application", "--timeout", "120"])
        else:
            subprocess.run(["gunicorn", "application", "--timeout", "120", "--reload"])