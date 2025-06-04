import random

from constants import DEFAULT_MASS, RHO_LIQUID, RHO_VAPOUR

from .molecule import Molecule


class Box:
    def __init__(self, x_range, y_range, z_range, density):
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
            M = Molecule(x, y, z, DEFAULT_MASS, 0)
            self.molecules.append(M)


class Liquid(Box):
    def __init__(self, x_range, y_range, z_range):
        super().__init__(x_range, y_range, z_range, RHO_LIQUID)


class Vapour(Box):
    def __init__(self, x_range, y_range, z_range):
        super().__init__(x_range, y_range, z_range, RHO_VAPOUR)


""" vi har lyst på:
- metode for å generere random tall
- metode for a populere
- metode for å returnere hvor mange molekyler som skal i hver boks
- childclasses
"""
