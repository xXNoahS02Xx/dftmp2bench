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
from dftmp2bench.parseTime import find_walltime

def find_out(software: str, directory: Path) -> list:
    """Find the output files and return them in a cronologically order list.
    If no output files are present return an empty list

    software: str
        - name of the software, either gaussian, psi4, xtb or orca
    directory: Path
        - path to the output file directory
    """
    if software in [Software.GAUSSIAN.value, Software.PSI4.value, Software.XTB.value]:
        output_ext = ".out"
    elif software in [Software.ORCA.value]:
        output_ext = ".property.json"
    output_list = list(directory.glob("*" + output_ext))
    if len(output_list) != 0:
        import os

        output_list.sort(key=lambda x: os.path.getmtime(x))
        return output_list
    return []


def get_output(software: str, directory: Path, name: str) -> dict:
    """
    finds natom, nmo and scfenergies from all output files and puts them in dict
    """
    basis = str(directory).split("/")[-1]
    level_of_theory = str(directory).split("/")[-2]
    molecule_name = str(directory).split("/")[-3]

    output_files_list = find_out(software, directory)
    if not output_files_list:
        print(
            f"*** Warning ***\n {name} output in directory {directory} is incomplete or contains errors. Output status = {output_files_list}"
        )

    if software == Software.ORCA.value:

        output_fns = [_ for _ in output_files_list if str(_).endswith(".property.json")]
        assert (
            len(output_fns) > 0
        ), f"json output missing from orca job ({name}, {directory}, {output_files_list})"
        name = str(output_fns[-1]).replace(".property.json", ".out")
        output = output_fns[-1]
        with open(directory / output) as f:
            data_dict = json.load(f)

        assert "Geometry_1" in data_dict.keys(), print(
            "Geometry_1 missing in ", data_dict.keys(), directory / output
        )
        assert "Calculation_Info" in data_dict["Geometry_1"].keys(), print(
            "Calculation_Info missing in",
            data_dict["Geometry_1"].keys(),
            directory / output,
        )
        # TODO: json should not exist if job is still running
        # print()
        # assert data_dict["Calculation_Status"]["STATUS"].upper()  == "RUNNING", f"Is the job {directory/output} still running?"
        assert "NORMAL" in data_dict["Calculation_Status"]["STATUS"].upper(), (
            f"Job {directory/output} did not terminate normally? "
            + "calc status:"
            + data_dict["Calculation_Status"]["STATUS"].upper()
        )

        termination = data_dict["Calculation_Status"]["STATUS"].upper()

        data_dict["nbasis"] = data_dict["Geometry_1"]["Calculation_Info"][
            "NUMOFBASISFUNCTS"
        ]
        data_dict["natom"] = data_dict["Geometry_1"]["Calculation_Info"]["NUMOFATOMS"]
        # data_dict["nmo"] = data_dict["Geometry_1"]["Calculation_Info"]["NUMOFBASISFUNCTS"]
        data_dict["scfenergies"] = data_dict["Geometry_1"]["Calculation_Info"][
            "TOTALENERGY"
        ]
        nbasis = data_dict["nbasis"]
        with open(directory / (str(name))) as f:
            wall_time = find_walltime(f.readlines())

    else:
        # not ORCA
        output_fns = [_ for _ in output_files_list if str(_).endswith(".out")]
        assert (
            len(output_fns) > 0
        ), f"json output missing from job, {output_fns}\nJob may still be running?"
        name = output_fns[-1]
        output = str(name)
        data_dict_cclib = cclib.io.ccread(directory / output)
        if software == Software.PSI4.value:
            output = "timer.dat"
        wall_time = find_walltime(open(directory / output).readlines())
        nbasis = data_dict_cclib.nbasis
        # TODO: actually check the termination status, will involve
        # loading the output since cclib doesn't store this info
        termination = "NORMAL TERMINATION"

    if software == Software.ORCA.value:
        scf_e = (
            data_dict["scfenergies"] * Hartree
        )  # converts from Hatree to eV according to ASE
    elif software == Software.XTB.value:
        scf_e = data_dict_cclib.scfenergies[-1]
    else:
        scf_e = data_dict_cclib.scfenergies[-1]

    if ("mp" in level_of_theory) and (software != Software.ORCA.value):
        scf_e = data_dict_cclib.mpenergies[-1]
    if ("cc" in level_of_theory) and (software != Software.ORCA.value):
        scf_e = data_dict_cclib.ccenergies[-1]

    # Prod
    output_dict = {
        "name": str(name),
        "molecule_name": molecule_name,
        "software": software,
        "wall_time": wall_time,
        "basis": basis,
        "level_of_theory": level_of_theory,
        "energy": scf_e,
        "nbasis": nbasis,
        "termination": termination,
    }

    return output_dict


# gpts object oriented approach for get_output
# import json
# from pathlib import Path
# import cclib
# from typing import Dict


# class JobOutput:
#     def __init__(self, software: str, directory: Path, name: str):
#         """
#         Initialize the JobOutput object with relevant details for a job.
#         """
#         self.software = software
#         self.directory = directory
#         self.name = name
#         self.basis = str(directory).split("/")[-1]
#         self.level_of_theory = str(directory).split("/")[-2]
#         self.molecule_name = str(directory).split("/")[-3]
#         self.output_files_list = self.find_out(software, directory)
#         self.data_dict = {}
#         self.nbasis = 0
#         self.scf_e = 0.0
#         self.termination = "NORMAL TERMINATION"
#         self.wall_time = 0.0

#     def find_out(self, software: str, directory: Path):
#         """
#         Find the output files for the given software in the specified directory.
#         This is a placeholder method, you should implement it as per your needs.
#         """
#         # Logic to find output files based on software
#         return [f for f in directory.glob("*") if f.suffix == '.out']  # Placeholder for actual logic

#     def process_orca_output(self):
#         """
#         Process output files from ORCA software.
#         """
#         output_fns = [f for f in self.output_files_list if f.endswith(".property.json")]
#         if not output_fns:
#             raise FileNotFoundError(f"JSON output missing from ORCA job ({self.name}, {self.directory})")

#         name = output_fns[-1].replace(".property.json", ".out")
#         output = output_fns[-1]

#         with open(self.directory / output) as f:
#             self.data_dict = json.load(f)

#         if "Geometry_1" not in self.data_dict:
#             raise KeyError(f"Geometry_1 missing in {self.directory / output}")
#         if "Calculation_Info" not in self.data_dict["Geometry_1"]:
#             raise KeyError(f"Calculation_Info missing in {self.directory / output}")

#         self.nbasis = self.data_dict["Geometry_1"]["Calculation_Info"]["NUMOFBASISFUNCTS"]
#         self.scf_e = self.data_dict["Geometry_1"]["Calculation_Info"]["TOTALENERGY"]
#         self.termination = self.data_dict["Calculation_Status"]["STATUS"].upper()

#         with open(self.directory / name) as f:
#             self.wall_time = self.find_walltime(f.readlines())

#     def process_non_orca_output(self):
#         """
#         Process output files for non-ORCA software.
#         """
#         output_fns = [f for f in self.output_files_list if f.endswith(".out")]
#         if not output_fns:
#             raise FileNotFoundError(f"Output file missing from job ({self.output_files_list}). Job may still be running?")

#         output = str(output_fns[-1])
#         data_dict_cclib = cclib.io.ccread(self.directory / output)

#         self.nbasis = data_dict_cclib.nbasis
#         self.termination = "NORMAL TERMINATION"

#         # Additional logic for PSI4, XTB, etc.
#         if self.software == "PSI4":
#             output = "timer.dat"
#         self.wall_time = self.find_walltime(open(self.directory / output).readlines())

#         self.scf_e = data_dict_cclib.scfenergies[-1]  # Example, adjust based on the software

#     def find_walltime(self, lines):
#         """
#         Find wall time from the output file lines.
#         Placeholder logic - adjust as per your actual wall time extraction needs.
#         """
#         # Simple placeholder to get wall time, implement actual logic to extract wall time
#         for line in lines:
#             if "Wall Time" in line:
#                 return float(line.split()[-1])
#         return 0.0

#     def get_output_dict(self) -> Dict:
#         """
#         Generate the output dictionary with job details.
#         """
#         if self.software == "ORCA":
#             self.process_orca_output()
#         else:
#             self.process_non_orca_output()

#         output_dict = {
#             "name": str(self.name),
#             "molecule_name": self.molecule_name,
#             "software": self.software,
#             "wall_time": self.wall_time,
#             "basis": self.basis,
#             "level_of_theory": self.level_of_theory,
#             "energy": self.scf_e,
#             "nbasis": self.nbasis,
#             "termination": self.termination,
#         }

#         return output_dict


# # Example Usage:
# # Initialize JobOutput for ORCA
# job = JobOutput(software="ORCA", directory=Path("/path/to/directory"), name="orca_job")
# output_dict = job.get_output_dict()
# print(output_dict)

# # Initialize JobOutput for other software (e.g., PSI4, XTB)
# job = JobOutput(software="PSI4", directory=Path("/path/to/directory"), name="psi4_job")
# output_dict = job.get_output_dict()
# print(output_dict)
