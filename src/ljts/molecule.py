class Molecule:
    def __init__(self, x, y, z, mass):
        self._x = x
        self._y = y
        self._z = z
        self._mass = mass

        # More instance variables
        self._U = 0.0
        self._fx = 0.0
        self._fy = 0.0
        self._fz = 0.0

        self._vx = 0.0
        self._vy = 0.0
        self._vz = 0.0

    def get_position(self):
        return self._x, self._y, self._z

    def get_mass(self):
        return self._mass

    def get_force(self):
        return self._fx, self._fy, self._fz

    def get_U(self):
        return self._U

    def get_acceleration(self):
        return (self._fx / self._mass, self._fy / self._mass, self._fz / self._mass)

    def get_velocity(self):
        return self._vx, self._vy, self._vz

    def set_velocity(self, vx, vy, vz):
        self._vx = vx
        self._vy = vy
        self._vz = vz

    # Added a incrementers for potential energy and so on

    def increment_U(self, nrg):
        self._U += nrg

    def increment_F(self, fx, fy, fz):
        self._fx += fx
        self._fy += fy
        self._fz += fz

    def reset_forces(self):
        self._fx = 0.0
        self._fy = 0.0
        self._fz = 0.0

    def __repr__(self):
        return f"{self._x}, {self._y}, {self._z}"
