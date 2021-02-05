from . import Force

# note: Input bond of RigidBondForce should be a Vector [atom1, atom2, bond_length]
class RigidBondForce(Force):
    def __init__(self, force_id=0, force_group=0) -> None:
        super().__init__(force_id, force_group)
        self._num_bonds = 0
        self._bonds = []
        self._bond_length = []

    def _addBond(self, bond):
        self._bonds.append(bond[:2])
        self._bond_length.append(bond[-1])
        self._num_bonds += 1

    def addBonds(self, *bonds):
        for bond in bonds:
            if len(bond) != 3:
                raise ValueError('The input RigidBondForce.addBonds should has three elements: [atom1, atom2, bond_length], instead of %d elements' %(len(bond)))
            self._addBond(bond)

    # todo: calculateEnergy, calculateForce
    def calculateEnergy(self):
        pass

    def calculateForce(self):
        pass

    @property
    def num_bonds(self):
        return self._num_bonds

    @property
    def bonds(self):
        return self._bonds

    @property
    def bond_length(self):
        return self._bond_length