import os

def current_dir_is_booyah_root():
    return os.path.exists(".booyah_version") and os.path.isfile(".booyah_version")

def booyah_src_path():
    if os.path.exists("../src"):
        return os.path.abspath("../src")
    return False

def booyah_lib_path():
    if os.path.exists("../src/lib"):
        return os.path.abspath("../src/lib")
    return False

def booyah_extensions_path():
    if os.path.exists("../src/lib/extensions"):
        return os.path.abspath("../src/lib/extensions")
    return False

def prompt_replace(target_path):
    if os.path.exists(target_path):
        response = input(f"'{target_path}' already exists. Do you want to replace it? (yes/no): ")
        if response.lower() == "yes":
            return True
        else:
            return False
    else:
        return True