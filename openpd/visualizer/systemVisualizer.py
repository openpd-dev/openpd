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

    def setGrid(self, flag:bool):
        self.grid = flag
        self.tick = flag

    def setTick(self, flag:bool):
        self.tick = flag

    def setLabel(self, flag:bool):
        self.label = flag

    def show(self):
        fig = plt.figure(figsize=self.figsize)
        #ax = Axes3D(fig)
        ax = fig.add_subplot(111, projection='3d')
        color = []
        for peptide in self.system.peptides:
            color.extend(['navy', 'brown'])
        ax.scatter(self.system.coordinate[:, 0], self.system.coordinate[:, 1], self.system.coordinate[:, 2], c=color, lw=10)
        for bond in self.system.topology.bonds:
            ax.plot([bond[0].coordinate[0], bond[1].coordinate[0]],
                    [bond[0].coordinate[1], bond[1].coordinate[1]],
                    [bond[0].coordinate[2], bond[1].coordinate[2]], c='teal', lw=2)
        if not self.grid:
            ax.grid(False)
        if not self.tick:
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([])
        if self.label:
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
        plt.show()
