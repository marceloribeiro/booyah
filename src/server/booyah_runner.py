import sys
import os
import subprocess

class BooyahRunner:
    def run_g(self):
        self.generate()

    def run_new(self):
        print("Creating a new project...")
        sys.path.append(self.src_path())
        from generators import generate_new
        generate_new.main(sys.argv[2:])

    def run_s(self):
        print("Starting server...")
        sys.path.append(self.src_path())
        from server.booyah_server import BooyahServer
        BooyahServer.run()

    def run_generate(self):
        print("Generating files and code...")
        sys.path.append(self.src_path())
        import generators
        generators.generate.main(sys.argv[2:])

    def run_c(self):
        """
        Starts python console by running generators/console.py to configure it
        """
        print("Starting booyah console...")
        self.require_under_virtual_env()
        python_command = f'PYTHONSTARTUP={self.src_path()}/generators/console.py python'
        subprocess.call(python_command, shell=True)
    
    def src_path(self):
        """
        src_path point to internal booyah module (using this booyah file to find the path)
        not a current booyah project path src
        '"""
        script_path = os.path.realpath(sys.argv[0])
        script_directory = os.path.dirname(script_path)
        return os.path.realpath(script_directory + '/../src')

    def require_under_virtual_env(self):
        """
        Verify if running this command under a virtual env
        """
        if "VIRTUAL_ENV" not in os.environ:
            print("Please run under a pyenv environment")
            print("i.e: pyenv activate booyah")
            sys.exit(1)