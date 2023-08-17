import sys
import os

def pytest_configure(config):
    print("****** Running conftest.py ******")

    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    src_path =  os.path.join(parent_dir, 'src')
    print(f'Adding src dir {src_path} to sys path')
    sys.path.insert(0, src_path)