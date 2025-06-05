class Molecule:
    def __init__(self, x, y, z, mass):
        self._x = x
        self._y = y
        self._z = z
        self._mass = mass
        self._U = 0.0

    def get_U(self):
        return self._U

    def get_position(self):
        return self._x, self._y, self._z

    def get_mass(self):
        return self._mass

    # Added a incrementer for potential energy
    def increment_U(self, nrg):
        self._U += nrg

    def __repr__(self):
        return f"{self._x}, {self._y}, {self._z}"
