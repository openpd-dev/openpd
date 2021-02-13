import pytest
from .. import Loader

class TestLoader:
    def setup(self):
        self.loader = Loader('test.json', 'json')

    def teardown(self):
        self.loader = None

    def  test_attributes(self):
        assert self.loader.input_file_path == 'test.json'

    def  test_exceptions(self):
        with pytest.raises(NotImplementedError):
            self.loader.loadSequence()

        with pytest.raises(NotImplementedError):
            self.loader.createSystem()