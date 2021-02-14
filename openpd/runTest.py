import pytest
import os
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(cur_dir, 'tests')

if __name__ == '__main__':
    pytest.main(['-s', '-r P', test_dir])