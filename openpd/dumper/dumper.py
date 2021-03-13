from ..exceptions import NonboundError, RebindError

class Dumper:
    def __init__(self, output_file, dump_interval:int, is_overwrite=True) -> None:
        self._output_file = output_file
        if is_overwrite:
            io = open(self._output_file, 'w')
            io.close()
        self._dump_interval = dump_interval
        self._is_bound = False
        
    def _test_bound(self):
        if not self._is_bound:
            raise NonboundError(
                'Dumper has not been bound to any Simulation!'
            )
            
    def bindSimulation(self, simulation):
        if self._is_bound == True:
            raise RebindError('Dumper has been bound to %s' %(self._simulation))
        self._simulation = simulation
        self._is_bound = True
        
    def dump(self):
        raise NotImplementedError('dump() method has not been overloaded yet!')
    
    @property
    def dump_interval(self):
        return self._dump_interval