#!/usr/bin/env python3
"""
Fix import resolution issues in Mode_0 project.
This script implements multiple solutions:
1. Patch the test files with import path fixes
2. Create a proper setup.py
3. Relocate test files to the tests directory
4. Install the package in development mode
"""
import os
import sys
import glob
import re
import shutil
import subprocess
from pathlib import Path

def find_project_root(start_dir='.'):
    """Find the project root directory by looking for mode_0 package."""
    current_dir = Path(os.path.abspath(start_dir))
    
    # Look for mode_0 directory with __init__.py to identify project root
    while current_dir != current_dir.parent:
        if (current_dir / 'mode_0' / '__init__.py').exists():
            return current_dir
        if (current_dir / 'Mode_0' / 'mode_0' / '__init__.py').exists():
            return current_dir
        current_dir = current_dir.parent
    
    raise FileNotFoundError("Unable to find project root (no mode_0 package found)")

def patch_test_file(test_file_path):
    """Add sys.path modification to a test file for import resolution."""
    with open(test_file_path, 'r') as f:
        content = f.read()
    
    # Check if the fix is already applied
    if "sys.path.insert" in content:
        print(f"Import fix already applied to {test_file_path}")
        return
    
    # Prepare import fix code
    import_fix = '''import sys
import os
# Add the parent directory to path so Python can find the mode_0 package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

'''
    
    # Add import fix after any initial docstrings and imports
    if content.startswith('"""') or content.startswith("'''"):
        # Find the end of the docstring
        match = re.search(r'(?:"""|\'\'\')(.*?)(?:"""|\'\'\')(?:\s*)', content, re.DOTALL)
        if match:
            insert_pos = match.end()
            patched_content = content[:insert_pos] + "\n" + import_fix + content[insert_pos:]
        else:
            patched_content = import_fix + content
    else:
        patched_content = import_fix + content
    
    # Write the modified content back
    with open(test_file_path, 'w') as f:
        f.write(patched_content)
    
    print(f"Applied import fix to {test_file_path}")
    return True

def create_setup_py(root_dir):
    """Create a setup.py file if it doesn't exist."""
    setup_py_path = os.path.join(root_dir, 'setup.py')
    
    if os.path.exists(setup_py_path):
        print("setup.py already exists")
        return
    
    setup_py_content = '''from setuptools import setup, find_packages

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
'''
    
    with open(setup_py_path, 'w') as f:
        f.write(setup_py_content)
    
    print(f"Created setup.py at {setup_py_path}")
    return True

def move_test_files(root_dir, test_files):
    """Move test files to the tests directory."""
    tests_dir = os.path.join(root_dir, 'tests')
    os.makedirs(tests_dir, exist_ok=True)
    
    for test_file in test_files:
        if os.path.dirname(test_file) == tests_dir:
            print(f"{test_file} is already in the tests directory")
            continue
        
        target_path = os.path.join(tests_dir, os.path.basename(test_file))
        
        # Check if a file with the same name already exists in the tests directory
        if os.path.exists(target_path):
            print(f"Warning: {target_path} already exists, skipping move")
            continue
        
        # Patch the file before moving
        patch_test_file(test_file)
        
        # Move the file
        shutil.copy2(test_file, target_path)
        print(f"Moved {test_file} to {target_path}")
    
    # Create an __init__.py file in the tests directory if it doesn't exist
    init_file = os.path.join(tests_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Tests package\n')
        print(f"Created {init_file}")
    
    print("Test files moved to tests directory")
    return True

def install_dev_package(root_dir):
    """Install the package in development mode."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=root_dir,
            check=True
        )
        print("Package installed in development mode")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing package: {e}")
        return False

def find_test_files(root_dir):
    """Find all test files in the project."""
    test_files = []
    
    # Look for files with "test_" prefix
    for filename in glob.glob(os.path.join(root_dir, "**", "test_*.py"), recursive=True):
        test_files.append(filename)
    
    # Also specifically look for test_mode_0.py
    mode_0_test_file = os.path.join(root_dir, "test_mode_0.py")
    if os.path.exists(mode_0_test_file) and mode_0_test_file not in test_files:
        test_files.append(mode_0_test_file)
    
    return test_files

def main():
    """Main function to fix import issues."""
    print("Mode_0 Import Resolution Fix Script")
    print("===================================")
    
    try:
        # Find the project root directory
        root_dir = find_project_root()
        print(f"Found project root: {root_dir}")
        
        # Find test files
        test_files = find_test_files(root_dir)
        if not test_files:
            print("No test files found.")
            return
            
        print(f"Found {len(test_files)} test file(s):")
        for test_file in test_files:
            print(f"  - {test_file}")
        
        print("\nChoose fix methods (multiple options can be selected):")
        print("1. Patch test files with import path fix")
        print("2. Create setup.py for development installation")
        print("3. Move test files to the tests directory")
        print("4. Install package in development mode")
        print("5. Apply all fixes")
        
        choice = input("Enter your choice(s) (e.g., 1,2,3): ").strip()
        choices = [int(c.strip()) for c in choice.split(',') if c.strip().isdigit()]
        
        if 5 in choices:
            choices = [1, 2, 3, 4]
        
        if 1 in choices or 3 in choices:
            for test_file in test_files:
                if 1 in choices and not 3 in choices:  # Only patch if not moving
                    patch_test_file(test_file)
        
        if 2 in choices:
            create_setup_py(root_dir)
        
        if 3 in choices:
            move_test_files(root_dir, test_files)
        
        if 4 in choices:
            if 2 in choices or os.path.exists(os.path.join(root_dir, 'setup.py')):
                install_dev_package(root_dir)
            else:
                print("Cannot install in development mode without setup.py")
                choice = input("Create setup.py now? (y/n): ").strip().lower()
                if choice == 'y':
                    create_setup_py(root_dir)
                    install_dev_package(root_dir)
        
        print("\nCompleted!")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
