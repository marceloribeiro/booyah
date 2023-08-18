import os

def current_dir_is_booyah_root():
    return os.path.exists(".booyah_version") and os.path.isfile(".booyah_version")
