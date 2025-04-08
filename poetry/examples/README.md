# PubMed Fetcher Examples

This directory contains example scripts demonstrating how to use the PubMed Fetcher package.

## Basic Usage

The `basic_usage.py` script shows how to:

- Initialize the PubMed Fetcher
- Search for papers
- Filter papers by company affiliation
- Convert results to a DataFrame
- Save results to a CSV file

Run it with:

```bash
python basic_usage.py
```

## Advanced Filtering

The `advanced_filtering.py` script demonstrates:

- Custom filtering by specific company names
- Grouping results by company
- More advanced data processing

Run it with:

```bash
python advanced_filtering.py
```

## Creating Your Own Examples

You can use these examples as a starting point for your own scripts. The PubMed Fetcher module provides a flexible API that can be used in various ways:

```python
from pubmed_fetcher import PubMedFetcher

# Initialize the fetcher
fetcher = PubMedFetcher(email="your.email@example.com")

# Search for papers
papers = fetcher.search(query="your query", max_results=100)

# Process the results
for paper in papers:
    print(f"Title: {paper.title}")
    print(f"Authors: {', '.join(paper.authors)}")
    print(f"Affiliations: {', '.join(paper.affiliations)}")
    print("---")
```

For more information, see the [main README](../README.md).
