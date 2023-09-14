class File:
    def __init__(self, file_path):
        self.file_path = file_path

    def __eq__(self, other):
        if isinstance(other, File):
            return self.file_path == other.file_path
        return False

    def __str__(self):
        return self.file_path
    
    def open(self, method='rb'):
        return open(self.file_path, method)