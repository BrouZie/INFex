import random

from constants import DEFAULT_MASS, RHO_LIQUID, RHO_VAPOUR, Lx, Ly, Lz

from .molecule import Molecule


class Box:
    def __init__(
        self, x_range: tuple, y_range: tuple, z_range: tuple, density: float
    ) -> None:
        self.min_range_x, self.max_range_x = x_range
        self.min_range_y, self.max_range_y = y_range
        self.min_range_z, self.max_range_z = z_range
        self.density = density

        self.molecules = []

    def get_volume(self):
        dx = self.max_range_x - self.min_range_x
        dy = self.max_range_y - self.min_range_y
        dz = self.max_range_z - self.min_range_z

        return dx * dy * dz

    # Lager tre tilfeldige floating verdier
    def _rand_position(self):
        rand_x = random.uniform(self.min_range_x, self.max_range_x)
        rand_y = random.uniform(self.min_range_y, self.max_range_y)
        rand_z = random.uniform(self.min_range_z, self.max_range_z)

        return rand_x, rand_y, rand_z

    # Finner ut hvor mange molekyler som skal plasseres i hver box
    def get_num_molecules(self):
        return int(round(self.density * self.get_volume()))

    def populate(self):
        num_m = self.get_num_molecules()
        for i in range(num_m):
            x, y, z = self._rand_position()
            M = Molecule(x, y, z, DEFAULT_MASS)
            self.molecules.append(M)

    def _get_minimum_distance(self, pos_i: list, pos_j: list):
        dx = pos_j[0] - pos_i[0]
        dy = pos_j[1] - pos_i[1]
        dz = pos_j[2] - pos_i[2]

        dx -= Lx * round(dx / Lx)
        dy -= Ly * round(dy / Ly)
        dz -= Lz * round(dz / Lz)

        return (dx**2 + dy**2 + dz**2) ** 0.5

    def _returns_potential(self, r):
        u_rcap = 2.5
        if r >= u_rcap:
            return 0.0

        u_LJ = 4 * (r ** (-12) - r ** (-6))
        u_LJ_rcap = 4 * (u_rcap ** (-12) - u_rcap ** (-6))
        return u_LJ - u_LJ_rcap

    # Changed postNrg to total_nrg, added the energy to each molecule object
    def compute_potential_u(self):
        total_nrg = 0.0
        pair_tot = 0.0
        # Resets the potential energy for each time compute is called
        for mol in self.molecules:
            mol._U = 0.0

        for i in range(len(self.molecules) - 1):
            pos_i = self.molecules[i].get_position()
            for j in range(i + 1, len(self.molecules)):
                pos_j = self.molecules[j].get_position()  # Sussy line....?
                # print(i, mol_i, mol_j)
                distance = self._get_minimum_distance(pos_i, pos_j)
                pair_nrg = self._returns_potential(distance)
                total_nrg += pair_nrg

                half_nrg = pair_nrg * 0.5
                self.molecules[i].increment_U(half_nrg)
                self.molecules[j].increment_U(half_nrg)

        for idx, mol in enumerate(self.molecules[:5]):
            print(f"Mol {idx} U = {mol.get_U()}")

        return total_nrg


class Liquid(Box):
    def __init__(self, x_range, y_range, z_range):
        super().__init__(x_range, y_range, z_range, RHO_LIQUID)


class Vapour(Box):
    def __init__(self, x_range, y_range, z_range):
        super().__init__(x_range, y_range, z_range, RHO_VAPOUR)
