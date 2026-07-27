# E-infra Examples

This repository contains small infrastructure examples that can be run locally with their own Python environment.

## Quick start

1. Create and activate a virtual environment in the repository root:
   - PowerShell:
     - `python -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
2. Install the dependencies for the first example:
   - `python -m pip install --upgrade pip`
   - `python -m pip install -r s3/requirements.txt`
3. Copy the S3 example environment template and fill in your credentials:
   - `Copy-Item s3/.env.example s3/.env`
   - Edit `s3/.env` with your S3 endpoint, access key, secret key and bucket name.

## Available examples

- S3 example: [s3/README.md](s3/README.md)