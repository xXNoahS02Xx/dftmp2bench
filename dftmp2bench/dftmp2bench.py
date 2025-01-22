import json
from pathlib import Path

import ccinput
from ccinput.wrapper import gen_input

current_dir = Path(__file__).parent
# read the directories json
with open(current_dir / ".." / "directories.json", "r") as f:
    directories = json.load(f)
print(directories)

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

softwares = ["orca", "gaussian", "psi4", "xtb"]

xyz_dir = current_dir / "data" / "xyzs"
xyzfilename = xyz_dir / "water.xyz"


def generate_input(software, xyz, basis, method, calc="sp", nproc=4):
    if software == "xtb":
        inp = gen_input(
            software=software,
            type=calc,
            method="GFN2-xTB",
            file=xyz,
            nproc=nproc,
        )
    else:
        inp = gen_input(
            software=software,
            type=calc,
            method=method,
            basis_set=basis,
            file=xyz,
            nproc=nproc,
        )
    return inp


def save_file(software, name, input_str, tag="calc"):
    file_dir = output_dir / tag / software
    if not file_dir.exists():
        file_dir.mkdir(parents=True)
    with open(file_dir / "{}.com".format(name), "w") as f:
        f.write(input_str)


def loop_softwares(xyz, basis, method):
    for software in softwares:
        inp = generate_input(software, xyz, basis, method)
        print(inp)
        save_file(software, "water", inp, "test")


loop_softwares(xyzfilename, "sto-3g", "hf")
