import pytest
from datetime import datetime
from typing import List, Dict
from pubmed_fetcher.pubmed_fetcher import PubMedFetcher, Paper

def test_is_non_academic_affiliation():
    fetcher = PubMedFetcher(email="test@example.com")
    
    # Test academic affiliations
    assert not fetcher._is_non_academic_affiliation("Harvard University")
    assert not fetcher._is_non_academic_affiliation("Medical Center Hospital")
    assert not fetcher._is_non_academic_affiliation("Research Institute")
    assert not fetcher._is_non_academic_affiliation("School of Medicine")
    
    # Test non-academic affiliations
    assert fetcher._is_non_academic_affiliation("Pfizer Pharmaceuticals")
    assert fetcher._is_non_academic_affiliation("Biotech Corp")
    assert fetcher._is_non_academic_affiliation("Pharmaceutical Company Ltd")
    assert fetcher._is_non_academic_affiliation("Biotechnology Research Center")

def test_extract_company_name():
    fetcher = PubMedFetcher(email="test@example.com")
    
    # Test company name extraction
    assert fetcher._extract_company_name("Pfizer Pharmaceuticals Inc.") == "Pfizer Pharmaceuticals Inc."
    assert fetcher._extract_company_name("Research at Biotech Corp Ltd") == "Biotech Corp Ltd"
    assert fetcher._extract_company_name("Novartis Pharma AG") == "Novartis Pharma AG"
    assert fetcher._extract_company_name("Merck & Co., Inc.") == "Merck & Co., Inc."
    
    # Test non-company affiliations
    assert fetcher._extract_company_name("University Hospital") is None
    assert fetcher._extract_company_name("Research Institute") is None
    assert fetcher._extract_company_name("Medical Center") is None

def test_extract_email():
    fetcher = PubMedFetcher(email="test@example.com")
    
    # Test with email
    authors = [
        {"LastName": "Smith", "ForeName": "John"},
        {"LastName": "Doe", "ForeName": "Jane", "Email": "jane.doe@company.com"}
    ]
    assert fetcher._extract_email(authors) == "jane.doe@company.com"
    
    # Test with multiple emails (should return first one)
    authors_multiple = [
        {"LastName": "Smith", "ForeName": "John", "Email": "john.smith@company.com"},
        {"LastName": "Doe", "ForeName": "Jane", "Email": "jane.doe@company.com"}
    ]
    assert fetcher._extract_email(authors_multiple) == "john.smith@company.com"
    
    # Test with no email
    authors_no_email = [{"LastName": "Smith", "ForeName": "John"}]
    assert fetcher._extract_email(authors_no_email) is None

def test_paper_creation():
    """Test Paper dataclass creation and properties."""
    paper = Paper(
        pubmed_id="12345",
        title="Test Paper",
        publication_date=datetime(2024, 1, 1),
        non_academic_authors=["John Smith", "Jane Doe"],
        company_affiliations=["Test Pharma Inc"],
        corresponding_author_email="test@example.com"
    )
    
    assert paper.pubmed_id == "12345"
    assert paper.title == "Test Paper"
    assert paper.publication_date == datetime(2024, 1, 1)
    assert paper.non_academic_authors == ["John Smith", "Jane Doe"]
    assert paper.company_affiliations == ["Test Pharma Inc"]
    assert paper.corresponding_author_email == "test@example.com"

@pytest.mark.integration
def test_fetch_papers():
    """Integration test for fetching papers."""
    fetcher = PubMedFetcher(email="test@example.com")
    
    # Test with a simple query
    papers = fetcher.fetch_papers("cancer drug", max_results=2)
    
    assert isinstance(papers, list)
    for paper in papers:
        assert isinstance(paper, Paper)
        assert paper.pubmed_id
        assert paper.title
        assert isinstance(paper.publication_date, datetime)
        assert isinstance(paper.non_academic_authors, list)
        assert isinstance(paper.company_affiliations, list)
        assert paper.corresponding_author_email is None or isinstance(paper.corresponding_author_email, str)
        
        # Verify that we only get papers with non-academic authors
        assert len(paper.non_academic_authors) > 0 