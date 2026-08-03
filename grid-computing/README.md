# Grid computing example

This example shows how to perform computations within Czech national computational grid.

## Usage and Basic Concepts

Prepare a computational setup, ideally a directory and run it using PBS script, see [an example](./run_script.pbs).
The example script is heavily commented, all the comments **except the header** can be deleted, but for this repo it is kept as instructive as possible.

Run the PBS script:
```bash
qsub run_script.pbs
```

More PBS commands can be found [in the Metacentrum documentation](https://docs.metacentrum.cz/en/docs/computing/resources/pbs-commands).

## PBS Script Header

The header is compulsory for PBS scripts; it specifies the resources needed for the job.

```bash
#!/bin/bash
#PBS -q default@pbs-m1.metacentrum.cz
#PBS -l walltime=24:00:0
#PBS -l select=1:ncpus=6:mem=3gb:scratch_local=2gb
```
The PBS Directives available for Metacentrum can be explored via [Qsub assembler](https://metavo.metacentrum.cz/pbsmon2/qsub_pbspro).


After submitting the job, it waits in the queue until resources are available, then it is assigned a scratch directory and executed.

### Scratch Directory

Scratch is space on the node's local disk, allowing efficient I/O operations. It is **not persistent** and should be cleaned after the job finishes. All results must be copied/moved back to the working directory.

### Key Environment Variables

- `SCRATCHDIR`: Absolute path of the scratch directory assigned to the job
- `PBS_O_WORKDIR`: Absolute path of the current working directory where `qsub` was run

## Module Management

Load required modules for your computation, e.g.:

```bash
module load openfoam/2112-gcc-10.2.1-iwn4u5v || { echo >&2 "Wasn't able to load OF!"; exit 1; }
module load gnuplot/5.4.3-gcc-10.2.1-enwslld || { echo >&2 "Wasn't able to load gnuplot!"; exit 1; }
```

### Important Notes on Modules

- Some modules require manual environment setup. For example, the OpenFOAM module does not set environment variables automatically:
  ```bash
  source $FOAM_ETC/bashrc
  ```
- If binaries are not in PATH, add them manually:
  ```bash
  export PATH=/storage/praha1/home/kreuzter/shared/Python-3.12.3/build/bin:$PATH
  ```

## Exit Codes

Exit codes are arbitrary and can be any integer in `[1; 255]`. Common exit statuses are documented at [Metacentrum docs](https://docs.metacentrum.cz/en/docs/computing/advanced#exit-status-interpretation).

They are shown in the personal view on the web. You can find out what was wrong just by opening a website.

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

The `-L` option follows symbolic links, copying actual files instead of links.

### 4. Run Computation

Keep actual commands in a separate script (e.g., `run.sh`) for better readability and local testing:

```bash
# Example OpenFOAM workflow
rm -r 0 || true                       
cp -r orig.0 0                           
decomposePar &>> log                          
mpirun -np 6 convLusgsFoam -parallel &>> log  
reconstructPar &>> log                        
```

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

Append job information to a file for debugging:

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
- Personal view (new and fancy): https://my.metacentrum.cz/
- Personal view (old but clear): https://metavo.metacentrum.cz/pbsmon2/user/ `user_name`
- Qsub assembler: https://metavo.metacentrum.cz/pbsmon2/qsub_pbspro


