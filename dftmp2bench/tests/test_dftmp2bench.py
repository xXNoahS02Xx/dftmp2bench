"""
Unit and regression test for the dftmp2bench package.

To run the tests, run `pytest` from the root directory of the repository.
"""

# Import package, test suite, and other packages as needed
import sys
from pathlib import Path

softwares = ["orca", "gaussian", "psi4", "xtb"]

import pytest

import dftmp2bench


def test_dftmp2bench_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "dftmp2bench" in sys.modules


def test_ccinput():
    import ccinput

    # current file directory
    current_dir = Path(__file__).parent
    xyzfilename = current_dir / ".." / "data" / "xyzs" / "water.xyz"

    from ccinput.wrapper import gen_input

    for software in softwares:
        if software == "xtb":
            inp = gen_input(
                software=software,
                type="sp",
                method="GFN2-xTB",
                file=xyzfilename,
                nproc=16,
            )
        else:
            inp = gen_input(
                software=software,
                type="sp",
                method="PBE0",
                basis_set="def2-SVP",
                file=xyzfilename,
                nproc=16,
            )
        print("SOFTWARE: ", software)
        print("*" * 80)
        print(inp)
        print("*" * 80)


if __name__ == "__main__":
    test_ccinput()
