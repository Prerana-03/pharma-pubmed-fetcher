#!/usr/bin/env python3
"""
Test script to verify company affiliation filtering functionality.
"""

from pubmed_fetcher import PubMedFetcher
import pandas as pd

def main():
    # Initialize the fetcher
    fetcher = PubMedFetcher(email="your.email@example.com")
    
    # Search for papers with a query that should return pharma company papers
    query = "cancer immunotherapy AND (Pfizer OR Merck OR Novartis OR Roche)"
    print(f"\nSearching for: {query}")
    
    # Get papers
    papers = fetcher.search(query=query, max_results=20)
    print(f"\nFound {len(papers)} total papers")
    
    # Filter papers by company affiliation
    filtered_papers = fetcher.filter_by_company_affiliation(papers)
    print(f"Found {len(filtered_papers)} papers with company affiliations")
    
    # Convert to DataFrame
    df = fetcher.to_dataframe(filtered_papers)
    
    # Display detailed results
    print("\nDetailed Results:")
    for _, row in df.iterrows():
        print(f"\nTitle: {row['Title']}")
        print(f"PubmedID: {row['PubmedID']}")
        print(f"Publication Date: {row['Publication Date']}")
        print(f"Non-academic Authors: {row['Non-academic Author(s)']}")
        print(f"Company Affiliations: {row['Company Affiliation(s)']}")
        print(f"Corresponding Author Email: {row['Corresponding Author Email']}")
    
    # Save to CSV
    output_file = "company_filter_test_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main() 