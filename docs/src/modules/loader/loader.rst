==============================
openpd.loader.Loader class
==============================

Overview
===========

The ``openpd.loader.Loader`` is the base class for all loaders in ``openpd.loader`` package. 

``Loader.guessCoordinates`` method is used to generate a straight peptide line that has the same sequence as ``Loader.sequence_dict``. 

In the peptide chain, the distance of :math:`C_\alpha\ -\ C_\alpha` is :math:`3.85 A` and distribute along :math:`x` axis. The distance between the mass center of the side chain (:math:`SC`) and its connected :math:`C_\alpha` is defined by the type of peptide. The :math:`SC\ -\ C_\alpha` bond is parallel to the :math:`YoZ` plane and the degree between :math:`SC\ -\ C_\alpha`  bond and :math:`y` axis is an evenly distributed random number in the range :math:`[-\pi, \pi)`.

.. seealso::

    The illustration of straight peptide chain:
    
    - :doc:`../../tutorials/howto_createSystem/main` Page
    - :doc:`pdbLoader` Page
    - :doc:`sequenceLoader` Page

Class methods
==============
.. automodule:: openpd.loader.loader
   :members:
   :undoc-members:
   :show-inheritance:


Examples
===========

Class inheritance
------------------

The users can define a custom loader by inherit ``Loader`` as below:

.. code-block:: python
    :linenos:

    import openpd as pd

    class SequenceLoader(pd.Loader):
        def __init__(self, input_file_path):
            super().__init__(input_file_path, 'json')
            self.loadSequence()

        def loadSequence(self):
            self.sequence_dict = {}
            ...... # Code to load the sequence from input file

        def createSystem(self):
            self.system = pd.System()
            ...... # Code to create a system
            self.guessCoordinates()
            return self.system

The code above is the code to define :doc:`sequenceLoader`. Basically, the users need to overload ``Loader.loadSequence()`` and ``Loader.createSystem`` to define a custom loader to meet more specific requirements. The user can also define new method to set coordinate. For example, we define a ``extractCoordinate()`` method in :doc:`pdbLoader` to extract coordinate from the *.pdb* file.