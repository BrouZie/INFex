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

        return total_nrg

    """
    This uses f_mag = - derivative of pair_nrg
    fx = f_mag * image_dx * 1/pair_nrg 

    """

    def compute_forces_F(self):
        # Reset before computation
        for mol in self.molecules:
            mol.reset_forces()

        for i in range(len(self.molecules) - 1):
            pos_i = self.molecules[i].get_position()
            for j in range(i + 1, len(self.molecules)):
                pos_j = self.molecules[j].get_position()

                dx = pos_j[0] - pos_i[0]
                dy = pos_j[1] - pos_i[1]
                dz = pos_j[2] - pos_i[2]
                dx -= Lx * round(dx / Lx)
                dy -= Ly * round(dy / Ly)
                dz -= Lz * round(dz / Lz)

                r = (dx**2 + dy**2 + dz**2) ** 0.5

                u_rcap = 2.5
                if r >= u_rcap:
                    continue

                duLJ_dr = 24.0 * r ** (-7) - 48.0 * r ** (-13)

                f_magnitude = -duLJ_dr

                inv_r = 1.0 / r
                fx = f_magnitude * dx * inv_r
                fy = f_magnitude * dy * inv_r
                fz = f_magnitude * dz * inv_r

                self.molecules[i].increment_F(fx, fy, fz)
                self.molecules[j].increment_F(-fx, -fy, -fz)

    def integrate(self, dt):
        """
        Perform one Velocity‐Verlet step of size dt:
        (1) Half‐step velocity: v(t+dt/2) = v(t) + (dt/2) * [F(t)/m]
        (2) Full‐step position:  x(t+dt) = x(t) + v(t+dt/2)*dt  (with PBC wrap)
        (3) Recompute forces at new positions → F(t+dt)
        (4) Complete velocity:  v(t+dt) = v(t+dt/2) + (dt/2) * [F(t+dt)/m]
        """

        # 1) HALF‐STEP VELOCITY
        for mol in self.molecules:
            fx, fy, fz = mol.get_force()  # F_i(t)
            m = mol.get_mass()
            # current velocity
            vx, vy, vz = mol.get_velocity()

            # v(t+dt/2) = v(t) + 0.5 * dt * (F(t)/m)
            vx += 0.5 * dt * (fx / m)
            vy += 0.5 * dt * (fy / m)
            vz += 0.5 * dt * (fz / m)

            mol.set_velocity(vx, vy, vz)

        # 2) FULL‐STEP POSITION + PBC WRAP
        for mol in self.molecules:
            vx, vy, vz = mol.get_velocity()

            # x(t+dt) = x(t) + v(t+dt/2)*dt
            mol._x += vx * dt
            mol._y += vy * dt
            mol._z += vz * dt

            # Wrap each coordinate into [0, L) using //
            mol._x %= Lx
            mol._y %= Ly
            mol._z %= Lz

        # 3) RECOMPUTE FORCES at new positions -> now F(t+dt)
        self.compute_forces_F()

        # 4) COMPLETE VELOCITY STEP
        for mol in self.molecules:
            fx, fy, fz = mol.get_force()  # Now F_i(t+dt)
            m = mol.get_mass()
            vx, vy, vz = mol.get_velocity()

            # v(t+dt) = v(t+dt/2) + 0.5 * dt * (F(t+dt)/m)
            vx += 0.5 * dt * (fx / m)
            vy += 0.5 * dt * (fy / m)
            vz += 0.5 * dt * (fz / m)

            mol.set_velocity(vx, vy, vz)


class Liquid(Box):
    def __init__(self, x_range, y_range, z_range):
        super().__init__(x_range, y_range, z_range, RHO_LIQUID)


class Vapour(Box):
    def __init__(self, x_range, y_range, z_range):
        super().__init__(x_range, y_range, z_range, RHO_VAPOUR)
