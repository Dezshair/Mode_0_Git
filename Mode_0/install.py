#!/usr/bin/env python3
import os
import sys
import subprocess
import venv
from pathlib import Path

ROOT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

def main():
    print("Setting up Mode_0 development environment...")
    
    # Create virtual environment
    venv_dir = ROOT_DIR / "venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
    
    # Get pip path
    if sys.platform == "win32":
        pip_path = venv_dir / "Scripts" / "pip"
    else:
        pip_path = venv_dir / "bin" / "pip"
    
    # Install dependencies
    print("Installing dependencies...")
    subprocess.check_call([str(pip_path), "install", "-e", "."])
    subprocess.check_call([str(pip_path), "install", "-r", "dev-requirements.txt"])
    
    print("\nSetup complete!")
    print(f"Activate virtual environment with:")
    if sys.platform == "win32":
        print(f"    {venv_dir}\Scripts\activate")
    else:
        print(f"    source {venv_dir}/bin/activate")

if __name__ == "__main__":
    main()
