#!/usr/bin/env python3
"""
Advanced example of using the PubMed Fetcher module with custom filtering.
"""

import pandas as pd
from pubmed_fetcher import PubMedFetcher, Paper

def filter_by_specific_companies(papers: list, company_names: list) -> list:
    """
    Filter papers by specific company names.
    
    Args:
        papers: List of Paper objects
        company_names: List of company names to filter by
        
    Returns:
        Filtered list of Paper objects
    """
    filtered_papers = []
    for paper in papers:
        # Check if any of the specified companies are in the paper's affiliations
        for company in company_names:
            if any(company.lower() in aff.lower() for aff in paper.affiliations):
                filtered_papers.append(paper)
                break
    return filtered_papers

def main():
    """Advanced example of using the PubMed Fetcher module."""
    # Initialize the fetcher
    fetcher = PubMedFetcher(email="your.email@example.com")
    
    # Search for papers
    query = "cancer AND immunotherapy"
    papers = fetcher.search(query=query, max_results=50)
    
    if not papers:
        print("No papers found")
        return
    
    # Filter papers by company affiliation
    company_papers = fetcher.filter_by_company_affiliation(papers)
    
    if not company_papers:
        print("No papers found with company affiliations")
        return
    
    # Further filter by specific companies
    specific_companies = ["Pfizer", "Merck", "Novartis", "Roche"]
    specific_company_papers = filter_by_specific_companies(company_papers, specific_companies)
    
    if not specific_company_papers:
        print(f"No papers found with affiliations from {', '.join(specific_companies)}")
        return
    
    # Convert to DataFrame
    df = fetcher.to_dataframe(specific_company_papers)
    
    # Group by company
    print(f"Found {len(specific_company_papers)} papers from specific companies:")
    for company in specific_companies:
        company_papers = [p for p in specific_company_papers 
                         if any(company.lower() in aff.lower() for aff in p.affiliations)]
        if company_papers:
            print(f"\n{company}: {len(company_papers)} papers")
            for paper in company_papers[:3]:  # Show first 3 papers
                print(f"  - {paper.title}")
    
    # Save to CSV
    df.to_csv("specific_company_results.csv", index=False)
    print("\nResults saved to specific_company_results.csv")

if __name__ == "__main__":
    main() 