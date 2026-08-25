# E-infra Examples

This repository contains small examples for working with e-INFRA CZ services,
including object storage, language models, and grid computing.

## Purpose

This repository provides ready-made, customized examples for selected e-INFRA
CZ services. You can copy individual examples as templates for your own work,
or clone the entire repository into another project and use it as a cookbook
for coding agents.

## Quick start

Each example is self-contained. Open its README first and follow the setup and
usage instructions there.

Python-based examples provide their own `requirements.txt` when additional
packages are needed. You can create one virtual environment in the repository
root and install only the requirements for the example you want to run:

```bash
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Or on PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install the selected example's dependencies, if it has a requirements
file:

```bash
python -m pip install --upgrade pip
python -m pip install -r <example>/requirements.txt
```

Some examples also require credentials or access to remote e-INFRA CZ
infrastructure. Their READMEs describe the required configuration.

## Available examples

- [S3 object storage](s3/README.md) - access S3-compatible storage from Python.
- [CESNET LLM API](llm/README.md) - send a chat request to an e-INFRA CZ
  language model.
- [Grid computing](grid-computing/README.md) - submit PBS jobs, use scratch
  storage, and run PyTorch on a GPU.
