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


class Software(Enum):
    PSI4 = "psi4"
    GAUSSIAN = "gaussian"
    ORCA = "orca"
    XTB = "xtb"



softwares = [
    "orca",
    # "gaussian",
]  # TODO: "psi4", "xtb" ]


basis_sets = [
    # "def2tzvpp",
    "def2svp",
    # "def2svpd",
    # "ccpvdz",
    # "ccpvdzpp",
    # "ccpvtzf12",
    # "631+gd",
    # "631+gdp",
    # "6311++g2d2p",
    # "sto3g",
]


methods = [
    # "hf",
    # "ccsd",
    # "r2scan-3c",
    # "b973c",
    #"mp2",
    #"rimp2",
    "pbe0",
    # "PBEh-3c",
    # "wb97xv",
    # "wb97xd3",
    # "wb97xd3bj",
    # "m062x",
    # "camb3lyp",
    # "b2plyp",
    # "dlpnoccsd",
    # "dlpnoccsdt",
]



def print_var(user, data_dir, output_dir):
    print("User:", user)
    print("Data:", data_dir)
    print("Output:", output_dir)
