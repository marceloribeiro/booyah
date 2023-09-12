BOLD = "\033[1m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

RESET = "\033[0m"

ERROR_CHAR = "❌"
SUCCESS_CHAR = "\033[32m✔\033[0m"

def make_bold(text):
    return f"{BOLD}{text}{RESET}"

def make_blue(text):
    return f"{BLUE}{text}{RESET}"

def print_error(message):
    print(f"{ERROR_CHAR} {message}")

def print_success(message):
    print(f"{SUCCESS_CHAR} {message}")

def prompt_override_file(file_path):
    return prompt_yes_no(f"The file '{file_path}' already exists. Do you want to override it? (yes/no): ")

def prompt_yes_no(message):
    choice = input(message).lower()
    return choice == "yes"