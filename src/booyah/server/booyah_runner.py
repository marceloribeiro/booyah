import sys
import os
import subprocess
from booyah.generators.helpers.system_check import booyah_path
from booyah.helpers.io import make_bold, make_blue

class BooyahRunner:
    def run_g(self):
        self.run_generate()

    def run_new(self):
        print("Creating a new project...")
        from booyah.generators.new_generator import NewGenerator
        NewGenerator(sys.argv[2:]).perform()

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
        Starts python console by running server/booyah_console.py to configure it
        """
        print("Starting booyah console...")
        self.require_under_virtual_env()
        python_command = f'PYTHONSTARTUP={booyah_path()}/server/booyah_console.py python'
        subprocess.call(python_command, shell=True)

    def require_under_virtual_env(self):
        """
        Verify if running this command under a virtual env
        """
        if "VIRTUAL_ENV" not in os.environ:
            print("Please run under a pyenv environment")
            print("i.e: pyenv activate booyah")
            sys.exit(1)
    
    def run_db(self):
        params = sys.argv[2:]
        environment = os.environ.get('BOOYAH_ENV', 'development')
        if not params:
            from booyah.db.adapters.base_adapter import BaseAdapter
            return BaseAdapter.open_client()
        db_operation = params[0]
        print(f'Running db {db_operation} in {make_blue(make_bold(environment))} environment')

        from booyah.server.booyah_database import BooyahDatabase
        getattr(BooyahDatabase(environment, params), f"{db_operation}_db")()