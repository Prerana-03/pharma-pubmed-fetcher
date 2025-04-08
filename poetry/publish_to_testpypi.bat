@echo off
REM Script to publish the package to Test-PyPI

REM Build the package
poetry build

REM Publish to Test-PyPI
poetry publish -r testpypi

echo Package published to Test-PyPI. You can install it with:
echo pip install --index-url https://test.pypi.org/simple/ pubmed-fetcher 

REM Keywords to identify academic institutions
academic_keywords = [
    "university", "college", "institute", "school", "hospital", 
    "medical center", "research center", "lab", "laboratory"
]

REM Keywords to identify pharmaceutical/biotech companies
company_keywords = [
    "pharmaceutical", "pharma", "biotech", "biotechnology", 
    "inc.", "ltd", "limited", "corporation", "corp"
] 