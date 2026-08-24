# Grid computing example

This example shows how to perform computations within Czech national computational grid.

## Before you Start

- You need to know your einfra `username` and `password`.
- You have to choose a frontend server from a [list](https://docs.metacentrum.cz/en/docs/computing/infrastructure/frontends). A frontend server is the only way to submit a task.

## Usage and Basic Concepts

1. Connect to frontend server via SSH `ssh <username>@<frontend>.metacentrum.cz`. 
   
   > You can use terminals available via OnDemand (*Frontend shell*) if not working on Linux and PuTTY is not your best friend. See [documentation](https://docs.metacentrum.cz/en/docs/graphical/ondemand).

2. Prepare a computational setup, ideally a directory and run it using PBS script, see `examples/`.
3. Place your task into a queue with PBS system 
    by running the PBS script:
    ```bash
    qsub run_script.pbs
    ```

> **Note:** You can run an interactive job (flag `-I`), which can be useful for testing or compilation:
> ```
> qsub -I -l walltime=0:30:00 \ -l select=1:ncpus=1:mem=1g:scratch_local=1
> ```

More PBS commands can be found [in the MetaCentrum documentation](https://docs.metacentrum.cz/en/docs/computing/resources/pbs-commands).

## PBS Script

There are example `.pbs` scripts in the `examples/` directory.
- While the [01_very_simple_job.pbs](./examples/01_very_simple_job.pbs) is just a toy script, 
- the [02_job_with_scratch.pbs](./examples/02_job_with_scratch.pbs) can already be used for something meaningful.
- [03_run_script.pbs](./examples/03_run_script.pbs) additionally handles sourcing variables needed for advanced runs with some defaultly ripped off modules.

### Header

The header is compulsory for PBS scripts; it replaces command line arguments and it specifies the resources needed for the job.

```bash
#!/bin/bash
#PBS -q default@pbs-m1.metacentrum.cz
#PBS -l walltime=24:00:0
#PBS -l select=1:ncpus=6:mem=3gb:scratch_local=2gb
```
The PBS Directives available for Metacentrum can be explored via [Qsub assembler](https://metavo.metacentrum.cz/pbsmon2/qsub_pbspro).

After submitting the job, it waits in the queue until resources are available, then it is assigned a scratch directory and executed.

> **Example:** Apart from the header, the PBS script is just a usual bash script.
> An overly simplified script is available as [01_very_simple_job.pbs](./examples/01_very_simple_job.pbs). It can be run safely from any directory as it just passively echoes some info.

### Scratch Directory

Scratch is space on the node's local disk, allowing efficient I/O operations. It is **not persistent** and should be cleaned after the job finishes (use `clean_scratch`). All results must be copied/moved back to the working directory before cleaning the scratch.

> **Example:** [02_job_with_scratch.pbs](./examples/02_job_with_scratch.pbs) shows basic manipulation with data on the scratch.
> Test that the scratch directory is set, load a module, copy your data to the scratch, cd there, do your job, copy the results back to working directory.

### Key Environment Variables

- `SCRATCHDIR`: Absolute path of the scratch directory assigned to the job
- `PBS_O_WORKDIR`: Absolute path of the current working directory where `qsub` was run

### Module Management

Load required modules for your computation, e.g.:

```bash
module add python36-modules-gcc
```
or
```bash
module load openfoam/2112-gcc-10.2.1-iwn4u5v || { echo >&2 "Wasn't able to load OF!"; exit 1; }
module load gnuplot/5.4.3-gcc-10.2.1-enwslld || { echo >&2 "Wasn't able to load gnuplot!"; exit 1; }
```

> **Notes on Modules and Binaries**
> - Some modules require manual environment setup. For example, the OpenFOAM module does not set environment variables automatically:
>  ```bash
>  source $FOAM_ETC/bashrc
>  ```
>- If binaries are not in PATH, add them manually:
>  ```bash
>  export PATH=/storage/praha1/home/kreuzter/shared/Python-3.12.3/build/bin:$PATH
>  ```

### Exit Codes

Exit codes are arbitrary and can be any integer in `[1; 255]`. Common exit statuses are documented at [Metacentrum docs](https://docs.metacentrum.cz/en/docs/computing/advanced#exit-status-interpretation).

They are shown in the [personal view](https://my.metacentrum.cz/) on the web. You can find out what was wrong just by opening the website.

## Recommended Workflow Pattern

### 1. Verify Scratch Directory

```bash
test -n "$SCRATCHDIR" || { echo >&2 "Variable SCRATCHDIR is not set!"; exit 2; }
```

### 2. Set Temporary Directory

Applications that write temporary files should use the scratch directory:

```bash
export TMPDIR=$SCRATCHDIR
```

### 3. Copy Input Files

Copy input files to scratch before running:

```bash
cp -rL $PBS_O_WORKDIR/* $SCRATCHDIR
cd $SCRATCHDIR
```

> **Note:** The `-L` option follows symbolic links, copying actual files instead of links. This is not compulsory, but protects the data on scratch from being changed from frontend and vice versa.

### 4. Run Computation

You can keep the actual commands in a separate script (e.g., `run.sh`) for better readability and local testing:

```bash
# Example OpenFOAM workflow
rm -r 0 || true                       
cp -r orig.0 0                           
decomposePar &>> log                          
mpirun -np 6 convLusgsFoam -parallel &>> log  
reconstructPar &>> log                        
```

Then in the `.pbs` script, just call the separate script:
```bash
./run.sh
```
> **Note:** Don't forget it needs correct permissions, you may need to use
> ```bash
> chmod +x run.sh
> ```

### 5. Post-processing

Run post-processing scripts (notice they can be located outside the scratch):

```bash
gnuplot /storage/brno2/home/kreuzter/scriptsAndSetups/gnuplotScripts/lusgs_residua.gp
```

### 6. Move Results Back

Transfer results from scratch to working directory. E.g.:

```bash
rm -r $PBS_O_WORKDIR/postProcessing || true
mv postProcessing $PBS_O_WORKDIR/
mv log $PBS_O_WORKDIR/
mv [1-9]* $PBS_O_WORKDIR/
mv *.png $PBS_O_WORKDIR/
```

### 7. Clean Scratch Directory

```bash
clean_scratch
```

**Note:** If the script is killed, the scratch directory is not cleaned automatically. Use `jobs_info.txt` to find the node and scratch directory for manual cleanup.

## Debugging and Tracking

At the beginning of the job append job information to a file for debugging:

```bash
echo "$PBS_JOBID is running on node `hostname -f` in a scratch directory $SCRATCHDIR" >> $PBS_O_WORKDIR/jobs_info.txt
```

If `jobs_info.txt` does not exist, it will be created. This helps track which node and scratch directory a job ran on.

## Manual Scratch Cleanup

If a job crashes or is killed, clean up manually:

```bash
ssh <node>
cd <scratch directory>
rm -rf *
```

## Reference Links

- General documentation: https://docs.metacentrum.cz/en/docs/computing/run-basic-job
- Personal view: https://my.metacentrum.cz/
- Qsub assembler: https://my.metacentrum.cz/qsub-assembler


