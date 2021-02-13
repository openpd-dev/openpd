==========================
openpd.core.Topology class
==========================

Overview
===========

``openpd.core.Topology`` is designed to store all the topology information of ``System``

.. seealso:: :doc:`system`

--------------------------------

.. image:: images/topology.svg
   :width: 700
   :align: center

--------------------------------

The topology of ``System`` contains atoms, bonds, angles, and torsions. In ``Topology``, the bonds, angles, and torsions are all defined as a ``list`` of ``Atom``. For example, a bond has the form: ``[atom1, atom2]``.

In OpenPD, the work of generating topology is accomplished based on several rules:

- Rule of **bonds**: the :math:`i`\ th peptide and :math:`i+1`\ th peptide has 3 bonds: one :math:`C_\alpha - C_\alpha` bond, and two :math:`SC-C\alpha` bonds. E.g: Bond :math:`1-0,\ 0-2,\ 2-3`.
- Rule of **angles**: the :math:`i`\ th peptide and :math:`i+1`\ th peptide has 2 angles: :math:`\angle SC-C_\alpha-C_\alpha` and :math:`\angle C_\alpha-C_\alpha-SC`. E.g: :math:`\angle 324,\ \angle 245`.
- Rule of **torsions**:  the :math:`i`\ th peptide and :math:`i+1`\ th peptide has 1 torsion: :math:`\angle SC-C_\alpha-C_\alpha-SC`. E.g: :math:`^2\angle 5467`

.. note:: 

   As ``Topology`` is always binding to a ``System`` instance and the topology rule is simple, the user will hardly create it manually, which is accomplished while adding ``Chain`` to the ``system``.

.. seealso::

   :doc:`system`

Class methods
==============

.. automodule:: openpd.core.topology
   :members:
   :undoc-members:
   :show-inheritance:

.. important::

   Read-only properties:

   - ``num_atoms``
   - ``atoms``
   - ``num_bonds``
   - ``bonds``
   - ``num_angles``
   - ``angles``
   - ``num_torsions``
   - ``torsions``

Example
==============

Instantiation
-------------

**Input**:

.. code-block:: python
   :linenos:

   import openpd as pd

   peptide1 = pd.Peptide('TYR')
   peptide2 = pd.Peptide('ASN')

   chain1 = pd.Chain()
   chain1.addPeptides(peptide1, peptide2)
   chain2 = pd.Chain()
   chain2.addPeptides(peptide2, peptide1)

   topology = pd.Topology()
   topology.addChains(chain1, chain2)

   print(topology)

**Output**:

.. parsed-literal::

   <Topology object: 8 atoms, 6 bonds, 4 angles, 2 torsions at 0x7fb09f523550>