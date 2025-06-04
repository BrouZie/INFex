from constants import (
    Y_LIQUID_MAX,
    Y_LIQUID_MIN,
    Y_VAPOUR_LEFT_MAX,
    Y_VAPOUR_RIGHT_MIN,
    Lx,
    Ly,
    Lz,
)
from src.ljts.box import Liquid, Vapour


def main():
    vap1 = Vapour(
        x_range=(0.0, Lx), y_range=(0.0, Y_VAPOUR_LEFT_MAX), z_range=(0.0, Lz)
    )

    liquid = Liquid(
        x_range=(0.0, Lx), y_range=(Y_LIQUID_MIN, Y_LIQUID_MAX), z_range=(0.0, Lz)
    )

    vap2 = Vapour(
        x_range=(0.0, Lx), y_range=(Y_VAPOUR_RIGHT_MIN, Ly), z_range=(0.0, Lz)
    )

    vap1.populate()
    liquid.populate()
    vap2.populate()

    n_vap1 = len(vap1.molecules)
    n_liquid = len(liquid.molecules)
    n_vap2 = len(vap2.molecules)

    n_total = n_vap1 + n_liquid + n_vap2

    for m in vap1.molecules:
        print(m)

    print("-" * 59)
    for m in liquid.molecules:
        print(m)

    print("-" * 59)
    for m in vap2.molecules:
        print(m)

    print("-" * 59)
    print(f"Total number of molecules: {n_total}")


if __name__ == "__main__":
    main()
