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


from dftmp2bench.constants import basis_sets
from dftmp2bench.constants import methods
from dftmp2bench.constants import print_var
from dftmp2bench.bench import make_csv
from dftmp2bench.bench import loop_jobs





current_dir = Path(__file__).parent
# read the directories json
with open(current_dir / ".." / "directories.json", "r") as f:
    directories = json.load(f)
# print(directories)

if "data" not in directories.keys():
    raise ValueError("Data directory not found in directories.json")
data_dir = Path(directories["data"])
# read the user
if "user" not in directories.keys():
    raise ValueError("User directory not found in directories.json")
user = Path(directories["user"])
if "output" not in directories.keys():
    raise ValueError("Output directory not found in directories.json")
output_dir = Path(directories["output"])
if "xtb" not in directories.keys():
    raise ValueError("XTB executable not found in directories.json")
xtb_exc = Path(directories["xtb"])


# TODO: add option to switch between dft, and post HF methods

#TODO: add option for different input file folders


xyz_dir = current_dir / ".." / "data" / "xyzs2"
xyzfilename = xyz_dir / "ala0.xyz"



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Write, run, and benchmark QM calculations"
    )

    parser.add_argument(
        "-s", "--script", type=str, required=True, help="script type = {input / ouput}"
    )

    parser.add_argument(
        "-t", "--tag", type=str, required=False, default="benchmark", help="tag"
    )

    parser.add_argument(
        "-fnr",
        "--fnr",
        type=str,
        required=False,
        default="*",
        help="regular expression to select filenames (fnr = filename-regrex)",
    )

    parser.add_argument(
        "-frz",
        "--frz",
        type=str,
        required=False,
        default=[],
        nargs="+",
        help="Freeze specified distance/angle/dihedral between the specified atoms, e.g. --frz 4-3-2 2-3 (has to be more than 1 and less than 5)",
    )

    parser.add_argument(
        "-np",
        "--nproc",
        type=int,
        required=False,
        default=1,
        help="number of processors",
    )
    parser.add_argument(
        "-m",
        "--mem",
        type=int,
        required=False,
        default=1000,
        help="amount of total memory in mB",
    )

    # TODO: by default, do all programs... but add an option to do only a selected group of programs
    # TODO: add option to switch between dft, and post HF methods

    args = parser.parse_args()
    print(args)
    print_var(user, data_dir, output_dir)


    #print("cli")########################################################################################
    dataframes = loop_jobs(args, xyz_dir, output_dir, current_dir, xtb_exc)



    if args.script == "output":
        df = make_csv(args, dataframes)
        print(df)
