# note: Evergy force has a force_id and an affiliated force_group
class Force(object):
    def __init__(self, force_id, force_group) -> None:
        """
        Parameters
        ----------
        force_id : int
            id of force
        force_group : int
            group id contains ``self`` 
        """        
        super().__init__()
        self._force_id = force_id
        self._force_group = force_group
        self._is_bound = False
        
    def bindEnsemble(self, ensemble):
        """
        bindEnsemble binds ``Force`` to an ``Ensemble``
        
        ``Force`` are only activated while calling ``bindEnsemble()``. This method will also be called when call ``Ensemble.addForces()``.

        Parameters
        ----------
        ensemble : Ensemble
            The target ``Ensemble`` instance to be bound

        Raises
        ------
        NotImplementedError
            When this method is not overloaded by subclass
        """        
        raise NotImplementedError('bindEnsemble() method has not been overloaded yet!')
    
    def _testBound(self):
        if self._is_bound == False:
            raise AttributeError(
                'Force has not been bound to any Ensemble!'
            )

    @property
    def force_id(self):
        """
        force_id gets the ``force_id`` of ``Force``

        Returns
        -------
        int
            the ``force_id`` of ``Force``
        """        
        return self._force_id

    @force_id.setter
    def force_id(self, force_id:int):
        self._force_id = force_id

    @property
    def force_group(self):
        """
        force_id gets the ``force_group`` of ``Force``

        Returns
        -------
        int
            the ``force_group`` of ``Force``
        """        
        return self._force_group

    @force_group.setter
    def force_group(self, force_group:int):
        self._force_group = force_group