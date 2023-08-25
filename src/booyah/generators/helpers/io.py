ERROR_CHAR = "❌"
SUCCESS_CHAR = "\033[32m✔\033[0m"

def print_error(message):
    print(f"{ERROR_CHAR} {message}")

def print_success(message):
    print(f"{SUCCESS_CHAR} {message}")

def prompt_override_file(file_path):
    return prompt_yes_no(f"The file '{file_path}' already exists. Do you want to override it? (yes/no): ")

def prompt_yes_no(message):
    choice = input(message).lower()
    return choice == "yes"