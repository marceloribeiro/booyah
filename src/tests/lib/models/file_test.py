from booyah.models.file import File

class TestFile:
    def test_should_return_file_path_as_str(self):
        file = File(__file__, {}, 0)
        assert str(file) == __file__