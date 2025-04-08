#!/bin/bash
# Script to publish the package to Test-PyPI

# Build the package
poetry build

# Publish to Test-PyPI
poetry publish -r testpypi

echo "Package published to Test-PyPI. You can install it with:"
echo "pip install --index-url https://test.pypi.org/simple/ pubmed-fetcher" 