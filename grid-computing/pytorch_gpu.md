# Running PyTorch on a GPU

This guide shows how to verify a MetaCentrum GPU allocation and run PyTorch in
an NVIDIA GPU Cloud (NGC) container. The accompanying probe checks the GPU,
CUDA-enabled PyTorch, network access, home-directory mounting, and the Python
environment inside the container.

## Prerequisites

- An active e-INFRA CZ account. Account details and password management are
  available in the [e-INFRA CZ profile](https://profile.e-infra.cz/profile).
- Access to a [MetaCentrum frontend](https://docs.metacentrum.cz/en/docs/computing/infrastructure/frontends).
- The files in this repository copied or cloned to a filesystem accessible from
  the frontend.

## Connect to a frontend

For example, connect to Tarkil over SSH:

```bash
ssh <username>@tarkil.grid.cesnet.cz
```

Replace `<username>` with your e-INFRA CZ username. You can use another
MetaCentrum frontend if preferred.

## Optional: request an interactive GPU job

An interactive allocation is useful for inspecting the environment or testing
commands before submitting a batch job:

```bash
qsub -I -l walltime=00:30:00 \
  -l select=1:ncpus=1:mem=1gb:scratch_local=1gb:ngpus=1:gpu_cap=compute_90
```

The `gpu_cap=compute_90` resource requests a GPU with CUDA compute capability
9.0. Remove or adjust this constraint when a different GPU generation is
suitable. The job may remain queued until matching resources are available.

Once the interactive job starts, commands run on the allocated compute node.
For example, verify the assigned GPU with:

```bash
nvidia-smi
```

Exit the shell when finished to release the allocation:

```bash
exit
```

## Run the probe as a batch job

The ready-to-use [`gpu_probe.pbs`](./examples/gpu_probe.pbs) script requests one GPU
on the `bee` cluster and runs PyTorch from the
`/cvmfs/singularity.metacentrum.cz/NGC/PyTorch:26.06-py3.SIF` Singularity
image. Review its PBS resource request and image path before submission, as
available clusters and images can change.

From the `grid-computing` directory, submit it with:

```bash
qsub examples/gpu_probe.pbs
```

`qsub` prints the job ID. Check the job state with:

```bash
qstat -u "$USER"
```

The script writes its report to a job-specific directory in your home
directory. Locate the newest report and read it with:

```bash
REPORT_DIR=$(ls -dt ~/h100_probe_* | head -n 1)
cat "$REPORT_DIR/report.txt"
```

The report should show that CUDA is available, identify the assigned GPU, and
end with `CUDA computation OK` after a matrix multiplication. It also records
connectivity checks and whether the home directory is visible from the
container.

## Customizing the job

- Change the `#PBS -l select=...` directive in `gpu_probe.pbs` to request different
  CPU, memory, scratch, GPU, or cluster resources.
- Change `IMAGE` to use another container from the
  [MetaCentrum container catalogue](https://docs.metacentrum.cz/en/docs/software/containers).
- Keep persistent results under `$HOME` or copy them from `$SCRATCHDIR` before
  the job ends. Scratch storage is temporary.
- Use `singularity exec --nv` whenever the command inside the container needs
  access to the allocated NVIDIA GPU.

For general PBS usage, scratch handling, and troubleshooting, see the
[grid-computing README](./README.md).
