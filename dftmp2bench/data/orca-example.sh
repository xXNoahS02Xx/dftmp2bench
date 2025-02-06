#!/bin/bash
##SBATCH --test-only    # Validate the batch script, job is not submitted.
## SBATCH -J orca # Job name
#SBATCH -o slurm.o%j    # Name of stdout output file
#SBATCH -e slurm.e%j    # Name of stderr error file
#SBATCH -p long       # Queue (partition) name
#SBATCH -N 1            # Total # of nodes (must be 1 for serial)
##SBATCH -n 4           # Total # of tasks (should be 1 for serial)
##SBATCH -t 48:00:00     # Run time (hh:mm:ss)

# expect to get jobname
hostname

echo $jobname

# Set some internal variables
JobDir="${SLURM_SUBMIT_DIR}"
JobName="${SLURM_JOB_NAME}"
InpExt="com"
InpDataExt=" hess inp GS.hess TS.hess ES.hess GS TS ES "
OutExt="out"
OutDataExt="property.json gbw prop xyz hess spectrum GS.hess TS.hess ES.hess GS TS ES "

SCRATCH=/scratch/schmidtn
# To run job on a nodes local filesystem change ${SCRATCH} to /tmp
ScrBase=${SCRATCH}
ScrDir="${ScrBase}/${SLURM_JOB_NAME}.${SLURM_JOB_ID}"

# Create job scratch directory
mkdir -p ${ScrDir}

# Prepend ORCA home directory to PATH and LD_LIBRARY_PATH
module load orca
ORCA_HOME=$ORCA_DIR

# Copy input/data files to ScrDir
for Ext in ${InpExt} ${InpDataExt} ; do
   if [ -e ${JobDir}/${JobName}.${Ext} ]; then
      cp -p ${JobDir}/${JobName}.${Ext} ${ScrDir}
   fi
done

# Change to scratch directory
cd ${ScrDir}

# Run ORCA
(/usr/bin/time -p ${ORCA_HOME}/orca ${JobName}.${InpExt} > ${JobName}.${OutExt})

# convert to json
orca_2json $JobName -property

# Copy output/data files to JobDir
for Ext in ${OutExt} ${OutDataExt} ; do
   if [ -e ${ScrDir}/${JobName}.${Ext} ]; then
      cp -p ${ScrDir}/${JobName}.${Ext} ${JobDir}
   fi
done

# List contents of ScrDir
du -sh ${ScrDir}
ls -ltr ${ScrDir}

# Delete ScrDir
rm -fr ${ScrDir}

exit
