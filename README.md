# fastapi-patient-backend

Brief workspace-level README describing folders and purpose.

## Overview
This repository contains two related projects:
- `patient-api` — a FastAPI-based backend serving patient-related functionality.
- `predict-insurance` — a small ML service and helper code to predict insurance (includes model, prediction logic and schema definitions).

There are also helper scripts at the repo root to create a virtual environment and install requirements on Windows.

## Folder / file summary

- patient-api/
  - main.py — FastAPI application entrypoint (defines Patient model / endpoints).
  - requirements.txt — Python dependencies used by the FastAPI app.
  - README.md — (per-service) documentation and usage for the FastAPI app.
  - ...other supporting files for the API service

- predict-insurance/
  - app.py — service entrypoint for the prediction service (API or script to serve predictions).
  - model/
    - predict.py — prediction helper that exposes `predict_output` (loads model and runs inference).
    - model.pkl — trained model artifact (binary). Consider excluding from git or using Git LFS.
  - schema/
    - user_input.py — `UserInput` pydantic/schema class used for input validation.
    - prediction_response.py — `PredictionResponse` schema for API responses.
  - frontend.py — a small client/interactive script to call the prediction service.
  - ...other helper files

- create_venv_and_install.bat — Windows CMD script: create venv, activate, upgrade pip, install `patient-api/requirements.txt`.
- create_venv_and_install.ps1 — PowerShell equivalent (shows messages and can bypass ExecutionPolicy).
- .gitignore (recommended) — ignore venv, __pycache__, model binaries, IDE files, etc.

## Quick setup

Windows (using provided script)
1. Open Command Prompt in the repository root.
2. Run:
   ```
   create_venv_and_install.bat
   ```
3. To activate later:
   ```
   venv\Scripts\activate.bat
   ```

PowerShell
1. Run (if ExecutionPolicy prevents running scripts, use the shown temporary bypass):
   ```
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\create_venv_and_install.ps1
   ```

Linux / macOS
1. Create venv and install:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r patient-api/requirements.txt
   ```

## How to run (examples)
- Run the FastAPI app (from repo root):
  ```
  uvicorn patient-api.main:app --reload --port 8000
  ```
- Run the prediction service app:
  - `uvicorn predict-insurance.app:app --reload --port 8001`

Adjust commands above depending on the actual entrypoints in each folder.

## Notes and recommendations
- The model artifact `predict-insurance/model/model.pkl` is a binary and can be large. Consider:
  - Adding it to `.gitignore` and storing it elsewhere.
  - Using Git LFS if you need it in the repo.
- Review and pin versions in `requirements.txt` before publishing.
- Add a repository-level `.gitignore` to exclude `venv/`, `*.pyc`, `__pycache__/`, `.vscode/`, and model binaries.

## Contact / next steps
- If you want, I can:
  - Produce a repository-level `.gitignore`.
  - Add a cross-platform venv creation script that accepts requirements file and venv name.
  - Create per-service README files with endpoint documentation and example requests.
