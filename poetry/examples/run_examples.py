#!/usr/bin/env python3
"""
Script to run all PubMed Fetcher examples.
This script will run all example scripts in the examples directory.
"""

import os
import sys
import importlib.util
import argparse
from typing import List, Optional

def run_example(example_path: str, email: str) -> None:
    """Run a single example script."""
    print(f"\nRunning {os.path.basename(example_path)}...")
    print("=" * 80)
    
    try:
        # Import the module
        spec = importlib.util.spec_from_file_location("example", example_path)
        if spec is None or spec.loader is None:
            print(f"Error: Could not load {example_path}")
            return
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run the example
        if hasattr(module, 'main'):
            if 'email' in module.main.__code__.co_varnames:
                module.main(email)
            else:
                module.main()
        else:
            print(f"Warning: No main() function found in {example_path}")
    
    except Exception as e:
        print(f"Error running {example_path}: {str(e)}")
    
    print("=" * 80)

def main():
    """Main function to run all examples."""
    parser = argparse.ArgumentParser(description="Run PubMed Fetcher examples")
    parser.add_argument("--email", required=True, help="Your email address (required by NCBI)")
    args = parser.parse_args()
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all Python files in the examples directory
    example_files = [
        os.path.join(script_dir, f)
        for f in os.listdir(script_dir)
        if f.endswith('.py') and f != 'run_examples.py'
    ]
    
    # Sort the files to ensure consistent order
    example_files.sort()
    
    print("Running PubMed Fetcher examples...")
    print(f"Using email: {args.email}")
    
    # Run each example
    for example_file in example_files:
        run_example(example_file, args.email)
    
    print("\nAll examples completed!")

if __name__ == "__main__":
    main() 