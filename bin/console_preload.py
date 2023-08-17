side_spaces = 20
initial_message = 'Welcome to Booyah Console'

message_length = len(initial_message)
formatted_line = '*' * (side_spaces * 2 + 2) + '*' * message_length

print(formatted_line)
print('*' + ' ' * side_spaces + initial_message + ' ' * side_spaces + '*')
print(formatted_line)

# Load required settings first
import sys
from py_dotenv import read_dotenv
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
dotenv_path = os.path.join(parent_dir, 'src', '.env')
read_dotenv(dotenv_path)
src_path =  os.path.join(parent_dir, 'src')
os.chdir(src_path)
sys.path.insert(0, src_path)

# Import libs that require previous settings

