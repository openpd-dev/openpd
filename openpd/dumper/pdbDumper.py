from . import Dumper

class PDBDumper(Dumper):
    def __init__(self, output_file, dump_interval,) -> None:
        super().__init__(output_file, dump_interval)