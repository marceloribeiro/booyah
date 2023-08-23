import os

def current_dir_is_booyah_root():
    return os.path.exists(".booyah_version") and os.path.isfile(".booyah_version")

def booyah_path():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(current_file_dir))
    return os.path.realpath(project_dir)

def prompt_replace(target_path):
    if os.path.exists(target_path):
        response = input(f"'{target_path}' already exists. Do you want to replace it? (yes/no): ")
        if response.lower() == "yes":
            return True
        else:
            return False
    else:
        return True