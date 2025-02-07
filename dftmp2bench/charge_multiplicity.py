from pathlib import Path
import ase
from ase import io
from ase import Atoms
import numpy as np

from dftmp2bench.cli import xyz_dir


def get_charge_multiplicity(atoms: ase.Atoms) -> (int, int):
    """see function name

    returns (int, int) for charge and multiplicity

    """
    nelec = sum(atoms.get_atomic_numbers())
    for charge in [0, 1, -1]:
        for multiplicity in [1, 2, 3, 4]:
            if verify_charge_mult(nelec, charge, multiplicity):
                return charge, multiplicity
    return None


def verify_charge_mult(electrons, charge, multiplicity):
    """Verifies that the requested charge and multiplicity are possible for the structure"""
    electrons -= charge
    odd_e = electrons % 2
    odd_m = multiplicity % 2
    return odd_e != odd_m


xyzs = list(Path(xyz_dir).glob("*.xyz"))

for _ in xyzs:
    atoms = ase.io.read(_)
    print(_)
    print(get_charge_multiplicity(atoms))
