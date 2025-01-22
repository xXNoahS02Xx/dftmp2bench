import json
import ase
from ase.units import Hartree
from pathlib import Path
import cclib
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
if "xtb" not in directories.keys():
    raise ValueError("XTB executable not found in directories.json")
xtb_exc = Path(directories["xtb"])

softwares = ["orca", "gaussian", "psi4", "xtb"]

xyz_dir = current_dir / "data" / "xyzs"
xyzfilename = xyz_dir / "water.xyz"


def generate_input(software, xyz, basis, method, calc="sp", nproc=1):
    print(xyz)
    if software == "xtb":
       o = str(xyz.name) + ".out"
       return f"{xtb_exc} {str(xyz)} > {o}" 
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


def raise_output_exists(out):
    raise ValueError("output {out} exists!")

def find_out(software, directory):
    if software in ["gaussian", "psi4", "xtb"]:
        output_ext = ".out"
    elif software in ["orca"]:
        output_ext = ".property.txt"
    output_list = list(directory.glob(".out"))
    if len(output_list) != 0:
        return output_list
    return False

def get_output(software, directory, name):
    o = find_out(software, directory)
    if software == "orca":
        output = str(name) + ".property.json"
        with open(directory / output) as f:
           data = json.load(f)
        print(data.keys())
        data["natom"] = data["Geometry_1"]["Calculation_Info"]["NUMOFATOMS"]
        data["nmo"] = data["Geometry_1"]["Calculation_Info"]["NUMOFBASISFUNCTS"]
        data["scfenergies"] = data["Geometry_1"]["Calculation_Info"]["TOTALENERGY"]
    else:
        output = str(name) + ".out"
        data = cclib.io.ccread(directory / output)
   
    print(software)
    print(output)
    print(dir(data))

    if software == "orca":
        print(data["scfenergies"]*Hartree)
    else:
        print(data.scfenergies)

    #print("There are %i atoms and %i MOs" % (data["natom"], data["nmo"]))

def save_file(software, method, basis, name, input_str, tag="calc"):
    if software == "xtb":
        file_dir = output_dir / tag / software / name 
    else:
        file_dir = output_dir / tag / software / name / method / basis 
    
    if not file_dir.exists():
        file_dir.mkdir(parents=True)

    fn = file_dir / f"{name}.com"
    if software == "xtb":
        fn = file_dir / "job.sh"
    
    if fn.exists():
        return
    if find_out(software, file_dir):
        print(f"{name} output file(s) already exist(s)")
        return 
    with open(fn, "w") as f:
        f.write(input_str)

    if software == "orca":
        job_str = f"module load orca; $ORCA_DIR/orca {name}.com > {name}.out; orca_2json {name} -property"
    if software == "gaussian":
        job_str = f"gsub {name}.com"
    if software == "psi4":
        job_str = f"conda activate p4env; psi4 {name}.com"
    
    fn = file_dir / "job.sh"
    if not software == "xtb":
        with open(fn, "w") as f:
            f.write(job_str)


def loop_softwares(xyz, basis, method, tag, script_type="output"):
    name = str(xyz.name)
    for software in softwares:
        if script_type == "input":
            inp = generate_input(software, xyz, basis, method)
            print(inp)
            save_file(software, method, basis, xyz.name, inp, tag)
        if script_type == "output":
            directory = output_dir / tag / software / name if software == "xtb" else output_dir / tag / software / name / method / basis
            get_output(software, directory, name)
            

def print_var():
    print("User:", user)
    print("Data:", data_dir)
    print("Output:", output_dir)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Write, run, and benchmark QM calculations")

    parser.add_argument("-s", "--script", type=str, required=True, help="script type = {input / ouput}")

    args = parser.parse_args()
    
    print_var()
    
    xyzs = list(Path(xyz_dir).glob("*.xyz"))

    loop_softwares(xyzs[0], "sto-3g", "hf", "test", script_type=args.script)


