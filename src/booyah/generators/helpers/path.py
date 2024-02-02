import os
from datetime import datetime

def new_migration_file_path(target_folder, file_name):
    counter = 0
    current_datetime = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    files_in_folder = os.listdir(target_folder)
    while True:
        counter_formatted = f"{counter:02d}"
        prefix = f"{current_datetime}{counter_formatted}_"
        already_exists = any(file.startswith(prefix) for file in files_in_folder)
        
        if not already_exists:
            return  os.path.join(target_folder, f"{prefix}{file_name}")
        
        counter += 1