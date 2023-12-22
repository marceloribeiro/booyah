import os
from booyah.framework import Booyah

def import_current_project_folder(target_sys):
    if Booyah.root:
        folder_to_add_sys = os.path.dirname(Booyah.root)
        target_sys.path.append(folder_to_add_sys)