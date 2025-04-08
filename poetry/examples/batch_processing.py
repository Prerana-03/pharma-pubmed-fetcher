#!/usr/bin/env python3
"""
Example demonstrating batch processing of multiple PubMed queries.
This script shows how to process multiple queries in parallel and combine results.
"""

import os
import sys
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

from pubmed_fetcher import PubMedFetcher

def process_query(query: str, email: str, max_results: int = 100) -> pd.DataFrame:
    """Process a single query and return results as DataFrame."""
    fetcher = PubMedFetcher(email=email)
    papers = fetcher.search(query=query, max_results=max_results)
    filtered_papers = fetcher.filter_by_company_affiliation(papers)
    return fetcher.to_dataframe(filtered_papers)

def batch_process_queries(queries: List[str], email: str, output_dir: str = "results") -> None:
    """Process multiple queries in parallel and save results."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process queries in parallel
    with ThreadPoolExecutor(max_workers=min(len(queries), 5)) as executor:
        futures = {
            executor.submit(process_query, query, email): query
            for query in queries
        }
        
        # Collect results
        all_results = []
        for future in futures:
            query = futures[future]
            try:
                df = future.result()
                if not df.empty:
                    # Add query information
                    df['Query'] = query
                    all_results.append(df)
                    
                    # Save individual results
                    safe_query = "".join(c if c.isalnum() else "_" for c in query)
                    output_file = os.path.join(output_dir, f"{safe_query}_results.csv")
                    df.to_csv(output_file, index=False)
                    print(f"Saved results for query '{query}' to {output_file}")
            except Exception as e:
                print(f"Error processing query '{query}': {str(e)}")
    
    # Combine all results
    if all_results:
        combined_df = pd.concat(all_results, ignore_index=True)
        combined_file = os.path.join(output_dir, "combined_results.csv")
        combined_df.to_csv(combined_file, index=False)
        print(f"\nSaved combined results to {combined_file}")
        print(f"Total papers found: {len(combined_df)}")
    else:
        print("No results found for any query.")

def main():
    """Main function to demonstrate batch processing."""
    if len(sys.argv) < 2:
        print("Usage: python batch_processing.py your.email@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    
    # Example queries
    queries = [
        "cancer immunotherapy",
        "diabetes treatment",
        "Alzheimer's disease",
        "COVID-19 vaccine",
        "genetic therapy"
    ]
    
    print("Processing queries in parallel...")
    batch_process_queries(queries, email)
    print("Done!")

if __name__ == "__main__":
    main() 