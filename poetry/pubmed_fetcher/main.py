#!/usr/bin/env python3
"""
Command-line interface for PubMed Fetcher.
"""

import logging
import sys
from typing import Optional

import click
import pandas as pd
from pubmed_fetcher.pubmed_fetcher import PubMedFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("query")
@click.option("--email", required=True, help="Your email address for NCBI")
@click.option(
    "--file",
    type=click.Path(),
    default="pubmed_results.csv",
    help="Output file path (CSV format)",
)
@click.option(
    "--max-results",
    type=int,
    default=100,
    help="Maximum number of results to return",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging",
)
def main(query: str, email: str, file: str, max_results: int, debug: bool) -> None:
    """
    Search PubMed and save results to a CSV file.
    
    QUERY: The search query to use (supports PubMed's full query syntax)
    
    The program will:
    1. Search PubMed for papers matching your query
    2. Filter for papers with non-academic authors
    3. Extract company affiliations
    4. Save results to a CSV file or print to console
    
    Output includes:
    - PubmedID: Unique identifier for the paper
    - Title: Title of the paper
    - Publication Date: Date the paper was published
    - Non-academic Author(s): Names of authors from non-academic institutions
    - Company Affiliation(s): Names of pharmaceutical/biotech companies
    - Corresponding Author Email: Email address of the corresponding author
    """
    try:
        # Initialize fetcher
        fetcher = PubMedFetcher(email=email, debug=debug)
        
        # Search PubMed
        logger.info(f"Searching PubMed for: {query}")
        papers = fetcher.search(query=query, max_results=max_results)
        
        if not papers:
            logger.warning("No papers found")
            return
        
        # Filter papers by company affiliation
        filtered_papers = fetcher.filter_by_company_affiliation(papers)
        
        if not filtered_papers:
            logger.warning("No papers found matching affiliation criteria")
            return
        
        # Convert to DataFrame
        df = fetcher.to_dataframe(filtered_papers)
        
        # Save to CSV
        df.to_csv(file, index=False)
        logger.info(f"Results saved to {file}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()
