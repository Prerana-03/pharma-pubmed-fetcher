# Pharma PubMed Fetcher

A Python package to fetch research papers from PubMed based on user-defined queries, specifically targeting papers affiliated with pharmaceutical or biotech companies.

[![PyPI version](https://badge.fury.io/py/pharma-pubmed-fetcher.svg)](https://badge.fury.io/py/pharma-pubmed-fetcher)
[![Python Version](https://img.shields.io/pypi/pyversions/pharma-pubmed-fetcher.svg)](https://pypi.org/project/pharma-pubmed-fetcher/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Search PubMed using custom queries with full PubMed query syntax support
- Filter papers by non-academic affiliations
- Extract company names from author affiliations
- Save results in CSV format with detailed information
- Command-line interface for easy usage
- Python API for programmatic access

## Installation

### From PyPI

```bash
pip install pharma-pubmed-fetcher
```

### From Source

```bash
git clone https://github.com/yourusername/pharma-pubmed-fetcher.git
cd pharma-pubmed-fetcher
poetry install
```

## Usage

### Command Line

```bash
get-papers-list "your search query" --email your.email@example.com --file output.csv
```

### Command Line Arguments

- `query`: Search query for PubMed (supports full PubMed query syntax)
- `--email`: Your email address (required by NCBI)
- `--file`: Output CSV file path (default: pubmed_results.csv)
- `--max-results`: Maximum number of results to return (default: 100)
- `--debug`: Enable debug mode for verbose output

### Python API

```python
from pubmed_fetcher import PubMedFetcher

# Initialize the fetcher
fetcher = PubMedFetcher(email="your.email@example.com")

# Search for papers
papers = fetcher.search(query="cancer AND immunotherapy", max_results=10)

# Filter papers by company affiliation
filtered_papers = fetcher.filter_by_company_affiliation(papers)

# Convert to DataFrame
df = fetcher.to_dataframe(filtered_papers)

# Save to CSV
df.to_csv("results.csv", index=False)
```

### Examples

The package includes example scripts demonstrating various use cases:

```bash
# Run all examples
python examples/run_examples.py --email your.email@example.com

# Run a specific example
python examples/basic_usage.py
python examples/advanced_filtering.py
```

See the [examples directory](examples/README.md) for more information.

## Output Format

The program generates a CSV file with the following columns:

- PubmedID: Unique identifier for the paper
- Title: Title of the paper
- Publication Date: Date the paper was published
- Non-academic Author(s): Names of authors affiliated with non-academic institutions
- Company Affiliation(s): Names of pharmaceutical/biotech companies
- Corresponding Author Email: Email address of the corresponding author

## Code Organization

The package is organized as follows:

- `pubmed_fetcher/`: Main package directory
  - `__init__.py`: Package initialization
  - `pubmed_fetcher.py`: Core functionality (module)
  - `main.py`: Command-line interface
- `tests/`: Test directory
  - `test_main.py`: Tests for the module
- `examples/`: Example scripts
  - `basic_usage.py`: Basic usage example
  - `advanced_filtering.py`: Advanced filtering example
  - `run_examples.py`: Script to run all examples
- `pyproject.toml`: Poetry configuration
- `setup.py`: Setuptools configuration (for compatibility)
- `requirements.txt`: Development dependencies

## Development

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pharma-pubmed-fetcher.git
cd pharma-pubmed-fetcher
```

2. Install development dependencies:

```bash
poetry install
```

3. Run tests:

```bash
poetry run pytest
```

4. Format code:

```bash
poetry run black pubmed_fetcher tests
poetry run isort pubmed_fetcher tests
```

5. Run linters:

```bash
poetry run flake8 pubmed_fetcher tests
poetry run mypy pubmed_fetcher
```

6. Check publication readiness:

```bash
python check_publication_readiness.py
```

## Publishing

### To PyPI

1. Create a PyPI account at https://pypi.org/
2. Configure Poetry with your PyPI credentials:

```bash
poetry config pypi-token.pypi your-token-here
```

3. Run the publish script:

On Linux/macOS:

```bash
chmod +x publish_to_pypi.sh
./publish_to_pypi.sh
```

On Windows:

```bash
publish_to_pypi.bat
```

### To Test-PyPI

1. Create a Test-PyPI account at https://test.pypi.org/
2. Configure Poetry to use Test-PyPI:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
```

3. Run the publish script:

On Linux/macOS:

```bash
chmod +x publish_to_testpypi.sh
./publish_to_testpypi.sh
```

On Windows:

```bash
publish_to_testpypi.bat
```

## Tools and Libraries Used

### Development Tools

- Python 3.10+
- Git for version control
- GitHub for repository hosting
- Poetry for dependency management
- Claude 3.5 Sonnet for code assistance and development

### Python Libraries

- [Biopython](https://biopython.org/) - For PubMed data retrieval
- [Click](https://click.palletsprojects.com/) - For command-line interface
- [Pandas](https://pandas.pydata.org/) - For data manipulation and CSV handling
- [Requests](https://requests.readthedocs.io/) - For HTTP requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
