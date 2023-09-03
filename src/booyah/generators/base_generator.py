import os
from booyah.generators.helpers.io import print_error, prompt_override_file

class BaseGenerator:
    def should_create_file(self):
        if os.path.exists(self.target_file):
            if prompt_override_file(self.target_file) == False:
                print_error(f'file already exists ({self.target_file})')
                return False
            else:
                os.remove(self.target_file)
                return True
        return True