#!/usr/bin/env python3
"""
Mode_0 Repository Cleanup and Optimization Tool

This script resolves common project issues:
1. Fixes directory structure and import paths
2. Standardizes imports across test files
3. Removes duplicate and temporary files
4. Ensures consistent module imports
5. Generates proper requirements files
6. Creates development tools for testing
"""

import os
import sys
import shutil
import re
import glob
import subprocess
import json
from pathlib import Path
from collections import defaultdict
import importlib.util

ROOT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
REQUIREMENTS = [
    "twitchio>=2.6.0",
    "aiohttp>=3.8.4",
    "sqlalchemy>=2.0.0",
    "apscheduler>=3.10.1",
    "websockets>=11.0.3",
    "python-dotenv>=1.0.0",
    "colorlog>=6.7.0",
]
DEV_REQUIREMENTS = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.20.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.10.0",
    "flake8>=6.0.0",
]

def fix_directory_structure():
    """Ensure directories follow Python best practices"""
    print("Fixing directory structure...")
    
    # Ensure the mode_0 package has consistent capitalization
    modes = list(ROOT_DIR.glob("*[mM][oO][dD][eE]_0*"))
    if len(modes) > 1:
        main_dir = next((d for d in modes if (d/"mode_0").exists()), None)
        if main_dir:
            for other_dir in modes:
                if other_dir != main_dir and other_dir.exists():
                    print(f"Removing duplicate directory: {other_dir}")
                    shutil.rmtree(other_dir)
    
    # Ensure package is in the root directory
    mode_0_dir = ROOT_DIR / "mode_0"
    if not mode_0_dir.exists() and (ROOT_DIR / "Mode_0" / "mode_0").exists():
        print("Moving mode_0 package to root...")
        shutil.move(str(ROOT_DIR / "Mode_0" / "mode_0"), str(ROOT_DIR))
        
    # Create required directories if missing
    for dir_name in ['logs', 'data', 'tests']:
        os.makedirs(ROOT_DIR / dir_name, exist_ok=True)

def fix_import_paths():
    """Fix import paths in all Python files"""
    print("Fixing import paths in Python files...")
    
    for py_file in ROOT_DIR.glob("**/*.py"):
        if py_file.is_file():
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove sys.path manipulation in test files
            if py_file.stem.startswith("test_"):
                content = re.sub(
                    r'import sys\nimport os\n# Add the parent directory to path.+?\)\)',
                    'import sys\nimport os',
                    content, 
                    flags=re.DOTALL
                )
            
            # Save changes
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)

def create_setup_files():
    """Create or update setup.py and other configuration files"""
    print("Creating setup files...")
    
    # Create setup.py if it doesn't exist
    setup_py = ROOT_DIR / "setup.py"
    if not setup_py.exists():
        with open(setup_py, 'w', encoding='utf-8') as f:
            f.write("""from setuptools import setup, find_packages

setup(
    name="mode_0",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "twitchio>=2.6.0",
        "aiohttp>=3.8.4",
        "apscheduler>=3.10.1",
        "websockets>=11.0.3",
        "python-dotenv>=1.0.0",
        "colorlog>=6.7.0",
        "sqlalchemy>=2.0.0",
    ],
    python_requires=">=3.11",
)
""")
    
    # Create requirements.txt
    with open(ROOT_DIR / "requirements.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(REQUIREMENTS) + '\n')
    
    # Create dev-requirements.txt
    with open(ROOT_DIR / "dev-requirements.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(DEV_REQUIREMENTS) + '\n')
    
    # Create pytest configuration
    with open(ROOT_DIR / "pytest.ini", 'w', encoding='utf-8') as f:
        f.write("""[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=mode_0
""")

def fix_test_imports():
    """Fix imports in test files"""
    print("Fixing test imports...")
    
    test_init = ROOT_DIR / "tests" / "__init__.py"
    if not test_init.exists():
        with open(test_init, 'w', encoding='utf-8') as f:
            f.write("# Test package\n")
    
    # Create conftest.py for shared test fixtures
    conftest = ROOT_DIR / "tests" / "conftest.py"
    if not conftest.exists():
        with open(conftest, 'w', encoding='utf-8') as f:
            f.write("""import pytest
import sys
import os

# Add the parent directory to path so Python can find the mode_0 package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def config_manager():
    from mode_0.config.config_manager import ConfigManager
    return ConfigManager()

@pytest.fixture
def mock_db():
    from unittest.mock import MagicMock, AsyncMock
    mock = MagicMock()
    mock.get_user_profile = AsyncMock(return_value={})
    mock.update_user_profile = AsyncMock()
    return mock
""")

def clean_temporary_files():
    """Clean up temporary and unwanted files"""
    print("Cleaning up temporary files...")
    
    # Remove temporary test reports
    for test_report in ROOT_DIR.glob("test_report_*.txt"):
        print(f"Removing test report: {test_report}")
        test_report.unlink()
    
    # Remove temporary config files
    for temp_config in ROOT_DIR.glob("temp_test_config.json"):
        print(f"Removing temporary config: {temp_config}")
        temp_config.unlink()
    
    # Remove __pycache__ directories
    for pycache in ROOT_DIR.glob("**/__pycache__"):
        print(f"Removing pycache: {pycache}")
        shutil.rmtree(pycache)
    
    # Remove compiled Python files
    for pyc in ROOT_DIR.glob("**/*.pyc"):
        print(f"Removing compiled Python file: {pyc}")
        pyc.unlink()

def create_dev_tools():
    """Create development helper scripts"""
    print("Creating development tools...")
    
    # Create install.py helper script
    with open(ROOT_DIR / "install.py", 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
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
    
    print("\\nSetup complete!")
    print(f"Activate virtual environment with:")
    if sys.platform == "win32":
        print(f"    {venv_dir}\\Scripts\\activate")
    else:
        print(f"    source {venv_dir}/bin/activate")

if __name__ == "__main__":
    main()
""")
    
    # Make it executable
    os.chmod(ROOT_DIR / "install.py", 0o755)
    
    # Create run.py for easy execution
    with open(ROOT_DIR / "run.py", 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
from mode_0.core.bot import Mode0Bot

def main():
    bot = Mode0Bot()
    bot.run()

if __name__ == "__main__":
    main()
""")
    
    # Make it executable
    os.chmod(ROOT_DIR / "run.py", 0o755)

def main():
    print("=== Mode_0 Repository Cleanup and Optimization Tool ===")
    fix_directory_structure()
    fix_import_paths()
    fix_test_imports()
    create_setup_files()
    clean_temporary_files()
    create_dev_tools()
    print("\nRepository cleanup and optimization complete!")
    print("\nNext steps:")
    print("1. Run './install.py' to set up the development environment")
    print("2. Activate the virtual environment")
    print("3. Run tests with 'pytest'")
    print("4. Run the bot with './run.py'")

if __name__ == "__main__":
    main()