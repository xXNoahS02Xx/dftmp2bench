from uuid import uuid1
import json
import ase
from ase.units import Hartree
from pathlib import Path
import cclib
import ccinput
from ccinput.wrapper import gen_input
from parseTime import parse_time_string
from enum import Enum
import polars as pl


class Software(Enum):
    PSI4 = "psi4"
    GAUSSIAN = "gaussian"
    ORCA = "orca"
    XTB = "xtb"

current_dir = Path(__file__).parent
# read the directories json
with open(current_dir / ".." / "directories.json", "r") as f:
    directories = json.load(f)
#print(directories)

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

softwares = ["orca", "gaussian", "psi4", "xtb" ]
basis_sets = ["def2tzvpp",
"def2svp",
"def2svpd",
#"madef2msvp",
#"madef2qzvp",
"ccpvdz",
"ccpvdzpp",
"ccpvtzf12",
#"ccpvtzppf12",
"631+gd",
"631+gdp",
"6311++g2d2p",
"sto3g",
#"sv",
#"svp",
]
methods = ["hf", "ccsd", "r2scan-3c", "b973c", "mp2", "rimp2",
        "pbe0", "PBEh-3c", "wb97xv", "wb97xd3", "wb97xd3bj", "m062x", 
        "camb3lyp", "b2plyp", "dlpnoccsd", "dlpnoccsdt", ]



xyz_dir = current_dir / "data" / "xyzs"
xyzfilename = xyz_dir / "ala0.xyz"

def find_walltime(lines):
    time_str = False
    line_numbers = [i for i,_ in enumerate(lines) if "time:" in _.lower()]
    assert len(line_numbers) > 0, "Error, no timings found!"
    #for _ in line_numbers:
    #    line_numbers.append(_+1)
    lines = [lines[i] for i in line_numbers]
    #print(lines)
    #print(lines[-1])
    times = [parse_time_string(_) for _ in lines if parse_time_string(_) is not None]
    #print(times)
    assert len(times) > 0, "Error, no timings found!"
    return max(times)



def generate_input(software, xyz, basis, method, calc="sp", nproc=1):
    #print(xyz)
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

def find_out(software: str, directory: Path) -> list:
    """Find the output files and return them in a cronologically order list. 
    If no output files are present return an empty list

    software: str 
        - name of the software, either gaussian, psi4, xtb or orca
    directory: Path
        - path to the output file directory
    """
    if software in ["gaussian", "psi4", "xtb"]:
        output_ext = ".out"
    elif software in ["orca"]:
        output_ext = ".property.json"
    output_list = list(directory.glob("*"+output_ext))
    if len(output_list) != 0:
        import os
        output_list.sort(key=lambda x: os.path.getmtime(x))
        return output_list
    return []

def get_output(software: str, directory: Path, name: str) -> dict:
    """
    """
    basis = str(directory).split("/")[-1]
    level_of_theory = str(directory).split("/")[-2]
    
    output_files_list = find_out(software, directory)
    if not output_files_list:
        print(f"*** Warning ***\n {name} output in directory {directory} is incomplete or contains errors. Output status = {output_files_list}")

    if software == Software.ORCA:
        #output = str(name) + ".property.json"
        #print(output_files_list) 
        output_fns = [_ for _ in output_files_list if str(_).endswith(".property.json")]
        assert len(output_fns) > 0, f"json output missing from orca job ({name}, {directory}, {output_files_list})"
        name = str(output_fns[-1]).replace(".property.json", ".out")
        output = output_fns[-1] 
        with open(directory / output) as f:
           data = json.load(f)
        
        assert "Geometry_1" in data.keys(), print("Geometry_1 missing in ", data.keys(), directory / output)
        assert "Calculation_Info" in data["Geometry_1"].keys(), print("Calculation_Info missing in", data["Geometry_1"].keys(), directory / output)
        # TODO: json should not exist if job is still running 
        assert data["Calculation_Status"]["STATUS"]  != "RUNNING", f"Is the job {directory/output} still running?"
        
        data["natom"] = data["Geometry_1"]["Calculation_Info"]["NUMOFATOMS"]
        data["nmo"] = data["Geometry_1"]["Calculation_Info"]["NUMOFBASISFUNCTS"]
        data["scfenergies"] = data["Geometry_1"]["Calculation_Info"]["TOTALENERGY"]
        #print("timings") 
        # timings
        with open(directory / (str(name))) as f:
            wall_time = find_walltime(f.readlines())
    else:
        output_fns = [_ for _ in output_files_list if str(_).endswith(".out")]
        assert len(output_fns) > 0, f"json output missing from orca job, {output_fns}\nJob may still be running?"
        name = output_fns[-1]
        output = str(name) 
        data = cclib.io.ccread(directory / output)
        if software == "psi4":
            output = "timer.dat"
        wall_time = find_walltime(open(directory / output).readlines())
        
    if software == "orca":
        scf_e = data["scfenergies"]*Hartree
    elif software == "xtb":
        scf_e = data.scfenergies[-1]
    else:
        scf_e = data.scfenergies[-1]

    if ("mp" in level_of_theory) and (software is not "orca"):
        scf_e = data.mpenergies[-1]
    if ("cc" in level_of_theory) and (software is not "orca"): 
        scf_e = data.ccenergies[-1]


    output_dict = {
            "name": str(name),
            "software": software,
            "wall_time": wall_time,
            "basis": basis,
            "level_of_theory": level_of_theory,
            "energy": scf_e 
            }

    return output_dict
    #print(name, "(", software, ")", "\t\t", wall_time, "secs", "\t", scf_e, "eV")

def save_file(software, method, basis, name, input_str, tag="calc"):
    if software == "xtb":
        file_dir = output_dir / tag / software / name 
    else:
        file_dir = output_dir / tag / software / name / method / basis 
    
    if not file_dir.exists():
        file_dir.mkdir(parents=True)

    name = f"{name}.{uuid1()}"
    fn = file_dir / (str(name )+".com")
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
        job_str = f"sbatch --wrap=\"{job_str}\""
    if software == "gaussian":
        job_str = f"gsub {name}.com"
    if software == "psi4":
        job_str = f"conda activate p4env; psi4 {name}.com"
        job_str = f"sbatch --wrap=\"{job_str}\""
    
    fn = file_dir / "job.sh"
    if not software == "xtb":
        with open(fn, "w") as f:
            f.write(job_str)


def loop_softwares(xyz, basis, method, tag, script_type="output") -> pl.DataFrame:
    name = str(xyz.name)
    job_output = []
    
    for software in softwares:
        if script_type == "input":
            inp = generate_input(software, xyz, basis, method)
            #print(inp)
            save_file(software, method, basis, xyz.name, inp, tag)
        if script_type == "output":


            directory = output_dir / tag / software / name if software == "xtb" else output_dir / tag / software / name / method / basis
            try:
                output_dictionary = get_output(software, directory, name)
                job_output.append(output_dictionary)

            except (AssertionError, AttributeError, json.decoder.JSONDecodeError) as e:
                print(f"Job: {software} {basis} {method} {name}")
                print(e)

    df = pl.DataFrame(job_output)
    return df




def print_var():
    print("User:", user)
    print("Data:", data_dir)
    print("Output:", output_dir)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Write, run, and benchmark QM calculations")

    parser.add_argument("-s", "--script", type=str, required=True, help="script type = {input / ouput}")
    parser.add_argument("-t", "--tag", type=str, required=False, default="benchmark", help="tag")

    args = parser.parse_args()
    
    print_var()
    
    dataframes = []

    xyzs = list(Path(xyz_dir).glob("*.xyz"))
    for xyz_ in xyzs:
        for bs in basis_sets:
            for m in methods:
                df = loop_softwares(xyzs[0], bs, m, args.tag, script_type=args.script)
                print(df)
                if len(df):
                    dataframes.append(df)

    print(dataframes)
    df = pl.concat(dataframes)

    # TODO: think of a better filename...
    df.write_csv(f"data.csv")
    print(df)

