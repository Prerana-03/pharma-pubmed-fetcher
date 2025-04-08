#!/usr/bin/env python3
"""
Script to run all PubMed Fetcher examples.
"""

import os
import sys
import importlib.util
import argparse

def run_example(example_path, email):
    """
    Run an example script with the provided email.
    
    Args:
        example_path: Path to the example script
        email: Email to use for NCBI
    """
    print(f"\n{'='*80}")
    print(f"Running example: {os.path.basename(example_path)}")
    print(f"{'='*80}\n")
    
    # Create a module from the script
    spec = importlib.util.spec_from_file_location("example_module", example_path)
    module = importlib.util.module_from_spec(spec)
    
    # Set the email in the module's namespace
    module.__dict__["email"] = email
    
    # Run the module
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error running example: {str(e)}")
    
    print("\n")

def main():
    """Run all examples."""
    parser = argparse.ArgumentParser(description="Run PubMed Fetcher examples")
    parser.add_argument("--email", required=True, help="Your email address for NCBI")
    args = parser.parse_args()
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all Python files in the examples directory
    example_files = []
    for file in os.listdir(script_dir):
        if file.endswith(".py") and file != "run_examples.py":
            example_files.append(os.path.join(script_dir, file))
    
    # Run each example
    for example_file in example_files:
        run_example(example_file, args.email)
    
    print("\nAll examples completed!")

if __name__ == "__main__":
    main() 