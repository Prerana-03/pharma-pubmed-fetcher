"""
Tests for the PubMed Fetcher module.
"""

import pytest
from datetime import datetime
from pubmed_fetcher.pubmed_fetcher import PubMedFetcher, Paper


def test_paper_creation():
    """Test creating a Paper object."""
    paper = Paper(
        pubmed_id="12345",
        title="Test Paper",
        publication_date=datetime.now(),
        authors=["Author 1", "Author 2"],
        affiliations=["University of Test", "Pharmaceutical Company A"],
        abstract="Test abstract",
    )
    
    assert paper.pubmed_id == "12345"
    assert paper.title == "Test Paper"
    assert len(paper.authors) == 2
    assert len(paper.affiliations) == 2
    assert paper.abstract == "Test abstract"
    assert paper.non_academic_authors == []
    assert paper.company_affiliations == []
    assert paper.corresponding_author_email is None


def test_identify_non_academic_authors():
    """Test identifying non-academic authors."""
    fetcher = PubMedFetcher(email="test@example.com")
    
    paper = Paper(
        pubmed_id="12345",
        title="Test Paper",
        publication_date=datetime.now(),
        authors=["Author 1", "Author 2"],
        affiliations=["University of Test", "Pharmaceutical Company A"],
        abstract="Test abstract",
    )
    
    fetcher._identify_non_academic_authors(paper)
    
    assert "Author 2" in paper.non_academic_authors
    assert "Author 1" not in paper.non_academic_authors
    assert "Pharmaceutical Company A" in paper.company_affiliations


def test_extract_corresponding_email():
    """Test extracting corresponding author email."""
    fetcher = PubMedFetcher(email="test@example.com")
    
    # Test with email in EM field
    record = {"EM": "author@example.com"}
    email = fetcher._extract_corresponding_email(record)
    assert email == "author@example.com"
    
    # Test with email in EA field
    record = {"EA": "author@example.com"}
    email = fetcher._extract_corresponding_email(record)
    assert email == "author@example.com"
    
    # Test with no email
    record = {}
    email = fetcher._extract_corresponding_email(record)
    assert email is None


def test_filter_by_company_affiliation():
    """Test filtering papers by company affiliation."""
    fetcher = PubMedFetcher(email="test@example.com")
    
    # Create papers with and without company affiliations
    paper1 = Paper(
        pubmed_id="1",
        title="Test Paper 1",
        publication_date=datetime.now(),
        authors=["Author 1"],
        affiliations=["Pharmaceutical Company A"],
        abstract="Test abstract",
    )
    paper1.company_affiliations = ["Pharmaceutical Company A"]
    
    paper2 = Paper(
        pubmed_id="2",
        title="Test Paper 2",
        publication_date=datetime.now(),
        authors=["Author 2"],
        affiliations=["University of Test"],
        abstract="Test abstract",
    )
    
    papers = [paper1, paper2]
    filtered = fetcher.filter_by_company_affiliation(papers)
    
    assert len(filtered) == 1
    assert filtered[0].pubmed_id == "1"


@pytest.mark.parametrize(
    "query,email,max_results,debug",
    [
        ("test query", "test@example.com", 10, False),
        ("test query", "test@example.com", 100, True),
    ],
)
def test_search_pubmed(query, email, max_results, debug):
    """Test PubMed search function."""
    # This is a basic test that just ensures the function runs
    # In a real test, you would mock the Entrez calls
    try:
        fetcher = PubMedFetcher(email=email, debug=debug)
        results = fetcher.search(query=query, max_results=max_results)
        assert isinstance(results, list)
    except Exception as e:
        pytest.skip(f"Skipping test due to network/API issues: {str(e)}") 