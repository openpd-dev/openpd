from . import Chain
from .. import CONST_CA_CA_DISTANCE
class Topology:
    def __init__(self) -> None:
        self._atoms = []
        self._bonds = []
        self._angles = []
        self._torsions = []
        self._num_atoms = 0
        self._num_bonds = 0
        self._num_angles = 0
        self._num_torsions = 0
    
    def __repr__(self) -> str:
        return ('<Topology object: %d atoms, %d bonds, %d angles, %d torsions at 0x%x>'
            %(self._num_atoms, self._num_bonds, self._num_angles, self._num_torsions, id(self)))

    __str__ = __repr__

    # note: Topology only record the topology information, didn't change any instance attributes
    def _addChain(self, chain:Chain):
        for i, peptide in enumerate(chain.peptides[:-1]):
            self._bonds.append([peptide.atoms[0], peptide.atoms[1], peptide.ca_sc_dist]) # Ca-Sc bond
            self._bonds.append([peptide.atoms[0], chain.peptides[i+1].atoms[0], CONST_CA_CA_DISTANCE]) # Ca- Ca bond
            self._num_bonds += 2

            self._angles.append([peptide.atoms[1], peptide.atoms[0], chain.peptides[i+1].atoms[0]]) # Sc - Ca - Ca
            self._angles.append([peptide.atoms[0], chain.peptides[i+1].atoms[0], chain.peptides[i+1].atoms[1]]) # Ca - Ca - Sc
            self._num_angles += 2

            self._torsions.append([peptide.atoms[1], peptide.atoms[0], chain.peptides[i+1].atoms[0], chain.peptides[i+1].atoms[1]])
            self._num_torsions += 1
        self._bonds.append([chain.peptides[-1].atoms[0], chain.peptides[-1].atoms[1], chain.peptides[-1].ca_sc_dist]) 
        self._num_bonds += 1
        self._atoms.extend(chain.atoms)
        self._num_atoms += chain.num_atoms

    def addChains(self, *chains):
        """
        addChains adds chains to the Topology

        Parameters
        ----------
        *chains : 
            one or serval Chain instance
        """  
        for chain in chains:
            self._addChain(chain)

    @property
    def num_atoms(self):
        """
        num_atoms gets the number of atoms in the topology

        Returns
        -------
        int
            the number of atoms in the topology
        """  
        return self._num_atoms

    @property
    def atoms(self):
        """
        atoms gets a ``list`` contain all atoms in the topology

        Returns
        -------
        list(Atom)
            list contain all atoms in the topology
        """ 
        return self._atoms

    @property
    def num_bonds(self):
        """
        num_bonds gets the number of bonds in the topology

        Returns
        -------
        int
            the number of bonds in the topology
        """  
        return self._num_bonds

    @property
    def bonds(self):
        """
        bonds gets a ``list`` contain all bonds in the topology

        a bond is also a list of atom like [atom1, atom2]

        Returns
        -------
        list(list(Atom))
            list contain all bonds in the topology
        """
        return self._bonds

    @property
    def num_angles(self):
        """
        num_angles gets the number of angles in the topology

        Returns
        -------
        int
            the number of angles in the topology
        """  
        return self._num_angles

    @property
    def angles(self):
        """
        angles gets a ``list`` contain all angles in the topology

        an angle is also a list of atom like [atom1, atom2, atom3] for :math:`\\angle 123` 

        Returns
        -------
        list(list(Atom))
            list contain all angles in the topology
        """
        return self._angles

    @property
    def num_torsions(self):
        """
        num_torsions gets the number of torsions in the topology

        Returns
        -------
        int
            the number of torsions in the topology
        """  
        return self._num_torsions

    @property
    def torsions(self):
        """
        torison gets a ``list`` contain all torsions in the topology

        a torsion is also a list of atom like [atom1, atom2, atom3, atom4] for :math:`^2\\angle 1234` 

        Returns
        -------
        list(list(Atom))
            list contain all torsions in the topology
        """
        return self._torsions

    

    
