from vpython import canvas, color, rate, sphere, vector

from constants import Lx, Ly, Lz
from src.ljts.box import Box, Liquid, Vapour


def visualize_box():
    vap1 = Vapour(x_range=(0.0, 5.0), y_range=(0.0, 16.0), z_range=(0.0, 5.0))
    liq = Liquid(x_range=(0.0, 5.0), y_range=(16.0, 24.0), z_range=(0.0, 5.0))
    vap2 = Vapour(x_range=(0.0, 5.0), y_range=(24.0, 40.0), z_range=(0.0, 5.0))

    vap1.populate()
    liq.populate()
    vap2.populate()

    all_molecules = vap1.molecules + liq.molecules + vap2.molecules
    box = Box((0.0, Lx), (0.0, Ly), (0.0, Lz), density=0.0)
    box.molecules = all_molecules

    scene = canvas(
        title="LJTS Molecules",
        width=800,
        height=600,
        center=vector(Ly / 2, Lx / 2, Lz / 2),
        background=color.white,
    )

    from vpython import box as vp_box

    # Our box:
    the_box = vp_box(
        pos=vector(Ly / 2, Lx / 2, Lz / 2),
        size=vector(Ly, Lx, Lz),
        opacity=0.05,
        color=color.gray(0.3),
    )

    spheres = []
    for mol in box.molecules:
        x, y, z = mol.get_position()
        s = sphere(pos=vector(y, x, z), radius=0.15, color=color.red)
        spheres.append(s)

    # need very small timestep
    dt = 0.01 * 10 ** (-3)
    # visual_scale = 0.2

    for step in range(1000):
        rate(100)
        box.integrate(dt)  # move by dt

        for idx, mol in enumerate(box.molecules):
            # newpos = vector(mol._x, mol._y, mol._z)
            # oldpos = spheres[idx].pos
            # spheres[idx].pos = oldpos + visual_scale * (newpos - oldpos)
            spheres[idx].pos = vector(mol._y, mol._x, mol._z)


if __name__ == "__main__":
    visualize_box()
