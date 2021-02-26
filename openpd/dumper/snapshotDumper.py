from . import Dumper

class SnapshotDumper(Dumper):
    def __init__(self, dump_interval) -> None:
        super().__init__(dump_interval)