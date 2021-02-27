class Dumper:
    def __init__(self, output_file, dump_interval:int) -> None:
        self._output_file = output_file
        io = open(self._output_file, 'w')
        io.close()
        self._dump_interval = dump_interval
        self._is_bound = False
        
    def _test_bound(self):
        if not self._is_bound:
            raise AttributeError(
                'Dumper has not been bound to any Simulation!'
            )
            
    def bindSimulation(self, simulation):
        if self._is_bound == True:
            raise AttributeError('Dumper has been bound to %s' %(self._simulation))
        self._simulation = simulation
        self._is_bound = True
        
    def dump(self):
        raise NotImplementedError('dump() method has not been overloaded yet!')
    
    @property
    def dump_interval(self):
        return self._dump_interval