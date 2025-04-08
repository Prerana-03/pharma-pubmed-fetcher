"""
Core functionality for PubMed Fetcher.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from Bio import Entrez
from Bio.Entrez import Parser

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class Paper:
    """Class representing a research paper from PubMed."""
    pubmed_id: str
    title: str
    publication_date: datetime
    authors: List[str]
    affiliations: List[str]
    abstract: str
    corresponding_author_email: Optional[str] = None
    non_academic_authors: List[str] = None
    company_affiliations: List[str] = None

    def __post_init__(self):
        """Initialize derived fields after initialization."""
        if self.non_academic_authors is None:
            self.non_academic_authors = []
        if self.company_affiliations is None:
            self.company_affiliations = []


class PubMedFetcher:
    """Class for fetching and processing papers from PubMed."""

    def __init__(self, email: str, debug: bool = False):
        """
        Initialize the PubMed Fetcher.

        Args:
            email: User's email for NCBI
            debug: Enable debug logging
        """
        self.email = email
        if debug:
            logger.setLevel(logging.DEBUG)
        
        # Set up Entrez
        Entrez.email = email

    def search(self, query: str, max_results: int = 100) -> List[Paper]:
        """
        Search PubMed with the given query and return results.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of Paper objects
        """
        # Search PubMed
        logger.info(f"Searching PubMed with query: {query}")
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        search_results = Entrez.read(handle)
        handle.close()

        if not search_results["IdList"]:
            logger.warning("No results found")
            return []

        # Fetch details for each paper
        logger.info(f"Fetching details for {len(search_results['IdList'])} papers")
        handle = Entrez.efetch(
            db="pubmed",
            id=search_results["IdList"],
            rettype="medline",
            retmode="text",
        )
        records = Entrez.parse(handle)

        papers = []
        for record in records:
            paper = self._parse_record(record)
            if paper:
                papers.append(paper)

        handle.close()
        return papers

    def _parse_record(self, record: Dict[str, Any]) -> Optional[Paper]:
        """
        Parse a PubMed record into a Paper object.

        Args:
            record: PubMed record dictionary

        Returns:
            Paper object or None if parsing fails
        """
        try:
            # Extract basic information
            pubmed_id = record.get("PMID", "")
            title = record.get("TI", "")
            authors = record.get("AU", [])
            affiliations = record.get("AD", [])
            abstract = record.get("AB", "")
            
            # Parse publication date
            pub_date_str = record.get("DP", "")
            try:
                # Try to parse the date, default to current date if parsing fails
                publication_date = datetime.strptime(pub_date_str, "%Y %b %d")
            except ValueError:
                try:
                    # Try alternative format
                    publication_date = datetime.strptime(pub_date_str, "%Y %b")
                except ValueError:
                    try:
                        # Try year only
                        publication_date = datetime.strptime(pub_date_str, "%Y")
                    except ValueError:
                        # Default to current date if all parsing attempts fail
                        publication_date = datetime.now()
            
            # Create Paper object
            paper = Paper(
                pubmed_id=pubmed_id,
                title=title,
                publication_date=publication_date,
                authors=authors,
                affiliations=affiliations,
                abstract=abstract,
            )
            
            # Identify non-academic authors and company affiliations
            self._identify_non_academic_authors(paper)
            
            # Extract corresponding author email
            paper.corresponding_author_email = self._extract_corresponding_email(record)
            
            return paper
        except Exception as e:
            logger.error(f"Error parsing record: {str(e)}")
            return None

    def _identify_non_academic_authors(self, paper: Paper) -> None:
        """
        Identify non-academic authors and company affiliations.

        Args:
            paper: Paper object to update
        """
        # Keywords to identify academic institutions
        academic_keywords = [
            "university", "college", "institute", "school", "hospital", 
            "medical center", "research center", "lab", "laboratory"
        ]
        
        # Keywords to identify pharmaceutical/biotech companies
        company_keywords = [
            "pharmaceutical", "pharma", "biotech", "biotechnology", 
            "inc.", "ltd", "limited", "corporation", "corp"
        ]
        
        # Process each author and their affiliation
        for i, author in enumerate(paper.authors):
            # Get affiliation for this author if available
            affiliation = ""
            if i < len(paper.affiliations):
                affiliation = paper.affiliations[i].lower()
            
            # Check if author is from a non-academic institution
            is_academic = any(keyword in affiliation for keyword in academic_keywords)
            if not is_academic and affiliation:
                paper.non_academic_authors.append(author)
            
            # Check for company affiliations
            if any(keyword in affiliation for keyword in company_keywords):
                # Extract company name (simplified approach)
                for keyword in company_keywords:
                    if keyword in affiliation:
                        # Try to extract company name (this is a simplified approach)
                        parts = affiliation.split(keyword)
                        if len(parts) > 1:
                            company = parts[0].strip()
                            if company:
                                paper.company_affiliations.append(company)
                            break

    def _extract_corresponding_email(self, record: Dict[str, Any]) -> Optional[str]:
        """
        Extract corresponding author email from the record.

        Args:
            record: PubMed record dictionary

        Returns:
            Email address or None if not found
        """
        # Try to find email in various fields
        email_fields = ["EM", "EA", "FAU"]
        for field in email_fields:
            if field in record:
                # Look for email pattern in the field
                import re
                email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
                matches = re.findall(email_pattern, str(record[field]))
                if matches:
                    return matches[0]
        
        return None

    def filter_by_company_affiliation(self, papers: List[Paper]) -> List[Paper]:
        """
        Filter papers to only include those with company affiliations.

        Args:
            papers: List of Paper objects

        Returns:
            Filtered list of Paper objects
        """
        return [paper for paper in papers if paper.company_affiliations]

    def to_dataframe(self, papers: List[Paper]) -> 'pandas.DataFrame':
        """
        Convert papers to a pandas DataFrame.

        Args:
            papers: List of Paper objects

        Returns:
            pandas DataFrame
        """
        import pandas as pd
        
        data = []
        for paper in papers:
            data.append({
                'PubmedID': paper.pubmed_id,
                'Title': paper.title,
                'Publication Date': paper.publication_date.strftime('%Y-%m-%d'),
                'Non-academic Author(s)': '; '.join(paper.non_academic_authors),
                'Company Affiliation(s)': '; '.join(paper.company_affiliations),
                'Corresponding Author Email': paper.corresponding_author_email or 'N/A'
            })
        
        return pd.DataFrame(data) 