from uuid import uuid1
import json
import ase
import shutil
from ase.units import Hartree
from pathlib import Path
import cclib
import ccinput
from ccinput.constants import SOFTWARE_BASIS_SETS
from ccinput.wrapper import gen_input
import dftmp2bench
from dftmp2bench.parseTime import parse_time_string
from enum import Enum
import polars as pl
import datetime
from dftmp2bench.constants import Software
# from dftmp2bench.cli import xtb_exc



def generate_input(
    software, xyz, basis, method, xtb_exc, calc="sp", nproc=1, mem=1000, frz=[]
) -> str:
    """Create the input file using ccinput"""
    if software == Software.XTB.value:
        o = str(xyz.name) + ".out"
        return f"{xtb_exc} {str(xyz)} > {o}"
    else:
        frz = [[int(i) for i in _.split("-")] for _ in frz]
        if len(frz) > 0:
            calc = "constr_opt"
        print(frz)
        inp = gen_input(
            software=software,
            type=calc,
            method=method,
            basis_set=basis,
            file=str(xyz),
            parse_name=True,
            nproc=nproc,
            mem=mem,
            freeze=frz,
        )
        # check B2PLYP
        if method == "b2plyp":
            _b = SOFTWARE_BASIS_SETS["orca"][basis]
            inp = inp.replace(_b, f"{_b} {_b}/C")
        # if yes, add
        print(inp)

    return inp
