from constants import Lx, Ly, Lz
from src.ljts.box import Box, Liquid, Vapour


def main():
    # Box = Create_Box() will be implemented later
    """
    Takes the sum of the number of molecules
    in each different type of box
    """
    vap1 = Vapour(x_range=(0.0, 5.0), y_range=(0.0, 16.0), z_range=(0.0, 5.0))

    liquid = Liquid(x_range=(0.0, 5.0), y_range=(16.0, 24.0), z_range=(0.0, 5.0))

    vap2 = Vapour(x_range=(0.0, 5.0), y_range=(24.0, 40.0), z_range=(0.0, 5.0))

    vap1.populate()
    liquid.populate()
    vap2.populate()

    mol_vap1 = len(vap1.molecules)
    mol_liquid = len(liquid.molecules)
    mol_vap2 = len(vap2.molecules)

    molecules_in_box = mol_vap1 + mol_liquid + mol_vap2
    print(f"The number of molecules in our box is: {molecules_in_box}")

    """
    Computes the potential energy,
    using the LJTS method
    """
    all_molecules_list = vap1.molecules + liquid.molecules + vap2.molecules

    box = Box((0.0, Lx), (0.0, Ly), (0.0, Lz), density=0)
    box.molecules = all_molecules_list
    print(f"The LJTS potential is: {box.compute_potential_u()}")


"""
tester pot per molekyl:

    # each_mol_count = 0
    # for molecule in box.molecules:
        # each_mol_count += molecule._U

    # print(each_mol_count)
"""

if __name__ == "__main__":
    main()
