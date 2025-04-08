#!/usr/bin/env python3
"""
Basic example of using the PubMed Fetcher module programmatically.
"""

import pandas as pd
from pubmed_fetcher import PubMedFetcher

def main():
    """Example of using the PubMed Fetcher module."""
    # Initialize the fetcher
    fetcher = PubMedFetcher(email="your.email@example.com")
    
    # Search for papers
    query = "cancer AND immunotherapy"
    papers = fetcher.search(query=query, max_results=10)
    
    if not papers:
        print("No papers found")
        return
    
    # Filter papers by company affiliation
    filtered_papers = fetcher.filter_by_company_affiliation(papers)
    
    if not filtered_papers:
        print("No papers found with company affiliations")
        return
    
    # Convert to DataFrame
    df = fetcher.to_dataframe(filtered_papers)
    
    # Display results
    print(f"Found {len(filtered_papers)} papers with company affiliations:")
    for _, row in df.iterrows():
        print(f"\nTitle: {row['Title']}")
        print(f"PubmedID: {row['PubmedID']}")
        print(f"Publication Date: {row['Publication Date']}")
        print(f"Non-academic Authors: {row['Non-academic Author(s)']}")
        print(f"Company Affiliations: {row['Company Affiliation(s)']}")
        print(f"Corresponding Author Email: {row['Corresponding Author Email']}")
    
    # Save to CSV
    df.to_csv("example_results.csv", index=False)
    print("\nResults saved to example_results.csv")

if __name__ == "__main__":
    main() 