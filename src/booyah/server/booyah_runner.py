import sys
import os
import subprocess
from booyah.generators.helpers.system_check import booyah_path

class BooyahRunner:
    def run_g(self):
        self.run_generate()

    def run_new(self):
        print("Creating a new project...")
        from booyah.generators import generate_new
        generate_new.main(sys.argv[2:])

    def run_s(self):
        print("Starting server...")
        from booyah.server.booyah_server import BooyahServer
        self.require_under_virtual_env()
        BooyahServer.run()

    def run_generate(self):
        print("Generating files and code...")
        from booyah.generators import generate
        generate.main(sys.argv[2:])

    def run_c(self):
        """
        Starts python console by running generators/console.py to configure it
        """
        print("Starting booyah console...")
        self.require_under_virtual_env()
        python_command = f'PYTHONSTARTUP={booyah_path()}/generators/console.py python'
        subprocess.call(python_command, shell=True)

    def require_under_virtual_env(self):
        """
        Verify if running this command under a virtual env
        """
        if "VIRTUAL_ENV" not in os.environ:
            print("Please run under a pyenv environment")
            print("i.e: pyenv activate booyah")
            sys.exit(1)