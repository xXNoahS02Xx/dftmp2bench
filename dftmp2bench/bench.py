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
from dftmp2bench.output import find_out
#from dftmp2bench.cli import output_dir
# from dftmp2bench.cli import current_dir
from dftmp2bench.constants import softwares
from dftmp2bench.input import generate_input
from dftmp2bench.output import get_output
# from dftmp2bench.cli import xyz_dir
# from dftmp2bench.cli import dataframes
# from dftmp2bench.cli import args
from dftmp2bench.constants import basis_sets
from dftmp2bench.constants import methods



def save_file(software, method, basis, output_dir, current_dir, name, input_str,  tag="calc", nproc=1, mem=1000):
    if software == Software.XTB.value:
        file_dir = output_dir / tag / software / name
    else:
        file_dir = output_dir / tag / software / name / method / basis

    if not file_dir.exists():
        file_dir.mkdir(parents=True)

    name = f"{name}.{uuid1()}"
    fn = file_dir / (str(name) + ".com")
    if software == Software.XTB.value:
        fn = file_dir / "job.sh"

    if fn.exists():
        return
    if find_out(software, file_dir):
        print(f"{name} output file(s) already exist(s)")
        return
    with open(fn, "w") as f:
        f.write(input_str)

    if software == Software.ORCA.value:
        # old method not using scratch
        # job_str = f"module load orca; $ORCA_DIR/orca {name}.com > {name}.out; orca_2json {name} -property"
        # job_str = f"sbatch --wrap=\"{job_str}\""

        # new method using the scratch dir
        # create the orca job script in the directory
        shutil.copyfile(
            current_dir / ".." / "data" / "orca-example.sh", file_dir / "orca.slurm"
        )
        job_str = f"sbatch -J {name} -n {nproc} --mem {mem} orca.slurm"  # where mem is mem per node in MB

    if software == Software.GAUSSIAN.value:
        job_str = f"gsub {name}.com"

    if software == Software.PSI4.value:
        job_str = f"conda activate p4env; psi4 {name}.com"
        job_str = f'sbatch --wrap="{job_str}"'

    fn = file_dir / "job.sh"
    if not software == Software.XTB.value:
        with open(fn, "w") as f:
            f.write(job_str)


def loop_softwares(
    xyz,
    basis,
    method,
    output_dir,
    current_dir,
    xtb_exc,
    tag,
    script_type="output",
    nproc=1,
    mem=1000,
    frz=[],
) -> pl.DataFrame | None:
    name = str(xyz.name)
    job_output = []



    for software in softwares:
        if script_type == "input":
            inp = generate_input(
                software, xyz, basis, method, xtb_exc, nproc=nproc, mem=mem, frz=frz
            )
            print("loop_softwares")
            save_file(software, method, basis, output_dir, current_dir, xyz.name, inp, tag, nproc=nproc, mem=mem)

        if script_type == "output":

            directory = (
                output_dir / tag / software / name
                if software == Software.XTB.value
                else output_dir / tag / software / name / method / basis
            )
            try:
                output_dictionary = get_output(software, directory, name)
                job_output.append(output_dictionary)

            except (AssertionError, AttributeError, json.decoder.JSONDecodeError) as e:
                print(f"ERROR -- Job: {software} {basis} {method} {name}")
                print("exception: ", e)

    if script_type == "output":
        df = pl.DataFrame(job_output)
        if df is not None:
            return df


def loop_jobs(args, xyz_dir, output_dir, current_dir, xtb_exc,):
    dataframes = []
    xyzs = list(Path(xyz_dir).glob(f"{args.fnr}"))
    #print("loop_jobs")#####################################################################################3
    for xyz_ in xyzs:
        #print(f"loop xyzs {xyz_}")############################################################################
        for bs in basis_sets:
            for m in methods:
                df = loop_softwares(
                    xyz_,
                    bs,
                    m,
                    output_dir,
                    current_dir,
                    xtb_exc,
                    args.tag,
                    script_type=args.script,
                    nproc=args.nproc,
                    mem=args.mem,
                    frz=args.frz,
                )
                if args.script == "output":
                    if len(df):
                        dataframes.append(df)
    return dataframes


def make_csv(args, dataframes):
    df = pl.concat(dataframes)
    date = datetime.date.today()
    df.write_csv(f"csvs/summary-{args.tag}-{date}-{uuid1()}.csv")
    return df
