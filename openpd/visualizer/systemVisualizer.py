import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SystemVisualizer(object):
    def __init__(self, system, figsize=[15, 10]) -> None:
        super().__init__()
        self.system = system
        self.figsize = figsize
        self.grid = False
        self.tick = False
        self.label = True

    def __repr__(self) -> str:
        return ('<SystemVisualizer object: %d atoms, %d bonds, at 0x%x>' 
            %(self.system.topology.num_atoms, self.system.topology.num_bonds, id(self)))

    __str__ = __repr__

    def show(
        self, atom_size=150, bond_width=3,
        is_grid=False, is_tick=True, is_legend=True, is_label=True
    ):
        fig = plt.figure(figsize=self.figsize)
        #ax = Axes3D(fig)
        ax = fig.add_subplot(111, projection='3d')
        color = []
        for peptide in self.system.peptides:
            color.extend(['navy', 'brown'])
        ax.scatter3D(
            self.system.coordinate[0::2, 0], self.system.coordinate[0::2, 1], self.system.coordinate[0::2, 2], 
            '.', c='navy', s=atom_size, edgecolors='face', label='\nCa\n'
        )
        ax.scatter3D(
            self.system.coordinate[1::2, 0], self.system.coordinate[1::2, 1], self.system.coordinate[1::2, 2], 
            '.', c='brown', s=atom_size, edgecolors='face',  label='\nSide chain center  \n'
        )
        # bond_x = []
        # bond_y = []
        # bond_z = []
        for bond in self.system.topology.bonds:
            # bond_x.extend([bond[0].coordinate[0], bond[1].coordinate[0]])
            # bond_y.extend([bond[0].coordinate[1], bond[1].coordinate[1]])
            # bond_z.extend([bond[0].coordinate[2], bond[1].coordinate[2]])
            ax.plot3D([bond[0].coordinate[0], bond[1].coordinate[0]],
                    [bond[0].coordinate[1], bond[1].coordinate[1]],
                    [bond[0].coordinate[2], bond[1].coordinate[2]], 
                    c='teal', lw=bond_width)
        # ax.plot3D(bond_x, bond_y, bond_z, c='teal', lw=bond_width, label='bond')
        if is_legend:
            ax.legend()
        if is_grid:
            ax.grid()
            is_tick = True
        else:
            ax.grid(False)
        if not is_tick:
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([])
        if is_label:
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
        plt.show()
