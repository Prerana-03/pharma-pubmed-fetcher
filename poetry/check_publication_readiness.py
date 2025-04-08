#!/usr/bin/env python3
"""
Script to check if the package is ready for publication.
"""

import os
import sys
import subprocess
import importlib.util

def check_file_exists(file_path):
    """Check if a file exists."""
    if os.path.exists(file_path):
        print(f"✅ {file_path} exists")
        return True
    else:
        print(f"❌ {file_path} does not exist")
        return False

def check_imports():
    """Check if all required packages can be imported."""
    required_packages = [
        "biopython",
        "click",
        "pandas",
        "requests",
    ]
    
    all_imported = True
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} can be imported")
        except ImportError:
            print(f"❌ {package} cannot be imported")
            all_imported = False
    
    return all_imported

def run_command(command):
    """Run a command and return the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    """Check if the package is ready for publication."""
    print("Checking if the package is ready for publication...\n")
    
    # Check required files
    required_files = [
        "README.md",
        "LICENSE",
        "pyproject.toml",
        "setup.py",
        "requirements.txt",
        "pubmed_fetcher/__init__.py",
        "pubmed_fetcher/pubmed_fetcher.py",
        "pubmed_fetcher/main.py",
        "tests/test_main.py",
        "examples/basic_usage.py",
        "examples/advanced_filtering.py",
        "examples/README.md",
    ]
    
    all_files_exist = True
    for file in required_files:
        if not check_file_exists(file):
            all_files_exist = False
    
    print("\nChecking imports...")
    all_imports_ok = check_imports()
    
    print("\nRunning tests...")
    tests_ok, test_output = run_command("poetry run pytest")
    if tests_ok:
        print("✅ Tests passed")
    else:
        print("❌ Tests failed")
        print(test_output)
    
    print("\nRunning linters...")
    linters_ok, linter_output = run_command("poetry run flake8 pubmed_fetcher tests")
    if linters_ok:
        print("✅ Linters passed")
    else:
        print("❌ Linters failed")
        print(linter_output)
    
    print("\nRunning type checker...")
    mypy_ok, mypy_output = run_command("poetry run mypy pubmed_fetcher")
    if mypy_ok:
        print("✅ Type checker passed")
    else:
        print("❌ Type checker failed")
        print(mypy_output)
    
    print("\nBuilding package...")
    build_ok, build_output = run_command("poetry build")
    if build_ok:
        print("✅ Package built successfully")
    else:
        print("❌ Package build failed")
        print(build_output)
    
    # Summary
    print("\nSummary:")
    if all_files_exist:
        print("✅ All required files exist")
    else:
        print("❌ Some required files are missing")
    
    if all_imports_ok:
        print("✅ All required packages can be imported")
    else:
        print("❌ Some required packages cannot be imported")
    
    if tests_ok:
        print("✅ Tests passed")
    else:
        print("❌ Tests failed")
    
    if linters_ok:
        print("✅ Linters passed")
    else:
        print("❌ Linters failed")
    
    if mypy_ok:
        print("✅ Type checker passed")
    else:
        print("❌ Type checker failed")
    
    if build_ok:
        print("✅ Package built successfully")
    else:
        print("❌ Package build failed")
    
    # Final recommendation
    if all_files_exist and all_imports_ok and tests_ok and linters_ok and mypy_ok and build_ok:
        print("\n✅ The package is ready for publication!")
        return 0
    else:
        print("\n❌ The package is not ready for publication. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 