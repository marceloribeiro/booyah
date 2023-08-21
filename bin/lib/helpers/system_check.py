import os

def current_dir_is_booyah_root():
    return os.path.exists(".booyah_version") and os.path.isfile(".booyah_version")

def booyah_lib_path():
    if os.path.exists("src/lib"):
        return os.path.abspath("src/lib")
    return False

def booyah_extensions_path():
    if os.path.exists("src/lib/extensions"):
        return os.path.abspath("src/lib/extensions")
    return False