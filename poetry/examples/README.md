# PubMed Fetcher Examples

This directory contains example scripts demonstrating how to use the PubMed Fetcher package.

## Basic Usage

The `basic_usage.py` script shows the simplest way to use the package:

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

## Advanced Filtering

The `advanced_filtering.py` script demonstrates more advanced filtering options:

```python
from pubmed_fetcher import PubMedFetcher

# Initialize the fetcher
fetcher = PubMedFetcher(email="your.email@example.com")

# Search with complex query
papers = fetcher.search(
    query="(cancer OR tumor) AND (immunotherapy OR immune therapy) AND 2023:2024[dp]",
    max_results=50
)

# Filter with custom criteria
filtered_papers = fetcher.filter_by_company_affiliation(
    papers,
    min_authors=2,
    require_email=True
)

# Convert to DataFrame with additional processing
df = fetcher.to_dataframe(filtered_papers)
df['Year'] = pd.to_datetime(df['Publication Date']).dt.year
```

## Batch Processing

The `batch_processing.py` script shows how to process multiple queries in parallel:

```python
from pubmed_fetcher import PubMedFetcher

# List of queries to process
queries = [
    "cancer immunotherapy",
    "diabetes treatment",
    "Alzheimer's disease",
    "COVID-19 vaccine",
    "genetic therapy"
]

# Process all queries in parallel
batch_process_queries(queries, email="your.email@example.com")
```

This script demonstrates:

- Parallel processing of multiple queries
- Saving individual results for each query
- Combining results into a single file
- Error handling for failed queries

## Running the Examples

To run all examples:

```bash
python examples/run_examples.py --email your.email@example.com
```

To run a specific example:

```bash
python examples/basic_usage.py
python examples/advanced_filtering.py
python examples/batch_processing.py your.email@example.com
```

## Creating Your Own Examples

You can create your own examples by following these templates. The PubMed Fetcher API is flexible and can be used in various ways:

```python
from pubmed_fetcher import PubMedFetcher

# Initialize the fetcher
fetcher = PubMedFetcher(email="your.email@example.com")

# Search for papers
papers = fetcher.search(query="your query here")

# Process the results
filtered_papers = fetcher.filter_by_company_affiliation(papers)
df = fetcher.to_dataframe(filtered_papers)

# Save or analyze the results
df.to_csv("your_results.csv", index=False)
```

For more information, see the [main README](../README.md).
