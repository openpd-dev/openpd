import pytest, os, argparse
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(cur_dir, 'tests')

parser = argparse.ArgumentParser(description='Input of test')
parser.add_argument('-n', type=int, default = 1)
args = parser.parse_args()

if __name__ == '__main__':
    pytest.main(['-s', '-r P', '-n %d' %args.n, test_dir])