import click
from .core import fetch_and_filter_papers

@click.command()
@click.option('--query', prompt='Enter PubMed search query', help='Search term for PubMed')
@click.option('--max-results', default=10, help='Maximum number of results to fetch')
@click.option('--output', default='results.csv', help='CSV file to save results')
@click.option('--email', prompt='Enter your email for NCBI', help='Email to use with Entrez API')
@click.option('--verbose', is_flag=True, help='Enable verbose logging')
def main(query, max_results, output, email, verbose):
    fetch_and_filter_papers(query, max_results, output, email, verbose)
