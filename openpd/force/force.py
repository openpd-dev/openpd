
# note: Evergy force has a force_id and an affiliated force_group
class Force(object):
    def __init__(self, force_id, force_group) -> None:
        super().__init__()
        self._force_id = force_id
        self._force_group = force_group

    @property
    def force_id(self):
        return self._force_id

    @force_id.setter
    def force_id(self, force_id:int):
        self._force_id = force_id

    @property
    def force_group(self):
        return self._force_group

    @force_group.setter
    def force_group(self, force_group:int):
        self._force_group = force_group