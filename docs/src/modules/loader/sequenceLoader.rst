===================================
openpd.loader.SequenceLoader class
===================================

Overview
===========

``openpd.loader.PDBLoader`` is designed to load a *.json* file and create a ``System`` instance.

The *.json* file have the form like:

.. code-block:: json
    :linenos:
    
    {
        "Chain 1": [
            "ASN", "ALA", "ASN", "ALA", "ALA",
            "ASN", "ALA", "ASN", "ALA", "ALA"
        ],
        "Chain 2": [
            "ASN", "ALA", "ASN", "ALA", "ALA"
        ]
    }

.. note::

    Each element that describes the peptide sequence in the *.json* file is a string list whose name starts with **Chain** (case insensitive), like: 

    - "Chain 1"
    - "CHAIN a"
    - "chain #"
  
    The word after **Chain** only plays the role of identification, while the order of chain solely depends on the writing order.

    The elements that do not start with  **Chain** will not be loaded into ``loader``.

.. note::

    Both three letter abbreviation and single letter abbreviation are supported in *.json* file by specific ``pd.SequenceLoader(pdb_file, is_single_letter=True)``. However, mixture styles like 

    .. code-block:: json
        
        {
            "Chain 1": ["ALA", "A"]
        }

    or 

    .. code-block:: json

        {
            "Chain 1": ["ALA", "ASN"],
            "Chain 2": ["A", "S"]
        }
        
    are not supported.


Class methods
==============
.. automodule:: openpd.loader.sequenceLoader
   :members:
   :undoc-members:
   :show-inheritance:


Example
=========

.. seealso::

   The usage of ``PDBLoader`` is discussed in :doc:`../../tutorials/howto_createSystem/main` Page