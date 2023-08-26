import os

def import_current_project_folder(target_sys):
    if os.environ["ROOT_PROJECT_PATH"]:
        folder_to_add_sys = os.path.dirname(os.environ["ROOT_PROJECT_PATH"])
        print(f'Adding to sys {folder_to_add_sys}')
        target_sys.path.append(folder_to_add_sys)