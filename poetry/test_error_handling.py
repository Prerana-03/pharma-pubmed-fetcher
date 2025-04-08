#!/usr/bin/env python3
"""
Test script to verify error handling and debug mode functionality.
"""

import logging
from pubmed_fetcher import PubMedFetcher

def test_invalid_email():
    """Test error handling for invalid email."""
    print("\nTesting invalid email handling...")
    try:
        fetcher = PubMedFetcher(email="invalid-email")
        print("❌ Should have raised ValueError for invalid email")
    except ValueError as e:
        print(f"✅ Correctly caught invalid email: {str(e)}")

def test_invalid_query():
    """Test error handling for invalid query."""
    print("\nTesting invalid query handling...")
    fetcher = PubMedFetcher(email="test@example.com")
    try:
        papers = fetcher.search(query="", max_results=10)
        print("❌ Should have raised ValueError for empty query")
    except ValueError as e:
        print(f"✅ Correctly caught empty query: {str(e)}")

def test_invalid_max_results():
    """Test error handling for invalid max_results."""
    print("\nTesting invalid max_results handling...")
    fetcher = PubMedFetcher(email="test@example.com")
    try:
        papers = fetcher.search(query="cancer", max_results=-1)
        print("❌ Should have raised ValueError for negative max_results")
    except ValueError as e:
        print(f"✅ Correctly caught negative max_results: {str(e)}")

def test_debug_mode():
    """Test debug mode functionality."""
    print("\nTesting debug mode...")
    
    # Set up logging to capture debug output
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("pubmed_fetcher")
    
    # Create fetcher with debug mode
    fetcher = PubMedFetcher(email="test@example.com", debug=True)
    
    # Verify debug mode is enabled
    if logger.getEffectiveLevel() == logging.DEBUG:
        print("✅ Debug mode is enabled")
    else:
        print("❌ Debug mode is not enabled")
    
    # Test search with debug mode
    try:
        papers = fetcher.search(query="cancer immunotherapy", max_results=5)
        print("✅ Search completed successfully with debug mode")
    except Exception as e:
        print(f"❌ Search failed with debug mode: {str(e)}")

def test_error_simulation():
    """Test error simulation in test mode."""
    print("\nTesting error simulation...")
    fetcher = PubMedFetcher(email="test@example.com", test_mode=True)
    
    # Test network error
    print("\nTesting network error simulation...")
    try:
        papers = fetcher.search(query="cancer", simulate_error='network')
        print("❌ Should have raised RuntimeError for network error")
    except RuntimeError as e:
        print(f"✅ Correctly caught network error: {str(e)}")
    
    # Test timeout error
    print("\nTesting timeout error simulation...")
    try:
        papers = fetcher.search(query="cancer", simulate_error='timeout')
        print("❌ Should have raised TimeoutError for timeout")
    except TimeoutError as e:
        print(f"✅ Correctly caught timeout error: {str(e)}")
    
    # Test parse error
    print("\nTesting parse error simulation...")
    try:
        papers = fetcher.search(query="cancer", simulate_error='parse')
        print("❌ Should have raised ValueError for parse error")
    except ValueError as e:
        print(f"✅ Correctly caught parse error: {str(e)}")

def main():
    """Run all error handling tests."""
    print("Running error handling and debug mode tests...")
    
    # Test invalid email
    test_invalid_email()
    
    # Test invalid query
    test_invalid_query()
    
    # Test invalid max_results
    test_invalid_max_results()
    
    # Test debug mode
    test_debug_mode()
    
    # Test error simulation
    test_error_simulation()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main() 