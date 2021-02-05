from .. import Force

class TestForce:
    def setup(self):
        self.force = Force(0, 0)
    
    def teardown(self):
        self.force = None

    def test_attributes(self):
        assert self.force.force_id == 0
        assert self.force.force_group == 0

    def test_exceptions(self):
        pass
