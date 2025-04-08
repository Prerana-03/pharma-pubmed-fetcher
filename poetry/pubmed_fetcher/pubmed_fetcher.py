"""
Core functionality for PubMed Fetcher.
"""

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from Bio import Entrez
from Bio.Entrez import Parser

if TYPE_CHECKING:
    import pandas as pd

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

    def __init__(self, email: str, debug: bool = False, test_mode: bool = False):
        """
        Initialize the PubMed Fetcher.

        Args:
            email: User's email for NCBI
            debug: Enable debug logging
            test_mode: Enable test mode for simulating failures

        Raises:
            ValueError: If email is invalid
        """
        if not self._is_valid_email(email):
            raise ValueError(f"Invalid email format: {email}")
            
        self.email = email
        self.test_mode = test_mode
        if debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")
        
        # Set up Entrez
        Entrez.email = email

    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            bool: True if email is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def search(self, query: str, max_results: int = 100, simulate_error: str = None) -> List[Paper]:
        """
        Search PubMed with the given query and return results.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            simulate_error: Type of error to simulate in test mode ('network', 'timeout', 'parse')

        Returns:
            List of Paper objects

        Raises:
            ValueError: If query is empty or max_results is invalid
            RuntimeError: If there's an error with the PubMed API
            TimeoutError: If the request times out
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")
            
        if max_results < 1:
            raise ValueError("max_results must be greater than 0")
            
        if max_results > 1000:
            logger.warning("max_results exceeds 1000, which may cause issues with PubMed API")
            
        # Simulate errors in test mode
        if self.test_mode and simulate_error:
            if simulate_error == 'network':
                raise RuntimeError("Simulated network error")
            elif simulate_error == 'timeout':
                raise TimeoutError("Simulated timeout error")
            elif simulate_error == 'parse':
                raise ValueError("Simulated parsing error")
            
        try:
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
                rettype="xml",
                retmode="xml"
            )
            
            # Parse the XML records
            papers = []
            records = Entrez.read(handle)
            for record in records.get("PubmedArticle", []):
                try:
                    paper = self._parse_xml_record(record)
                    if paper:
                        papers.append(paper)
                except Exception as e:
                    logger.error(f"Error parsing record: {str(e)}")
            handle.close()
            
            return papers
            
        except TimeoutError as e:
            error_msg = f"Request timed out: {str(e)}"
            logger.error(error_msg)
            raise TimeoutError(error_msg)
        except Exception as e:
            error_msg = f"Error searching PubMed: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def _parse_xml_record(self, record: Dict[str, Any]) -> Optional[Paper]:
        """
        Parse a PubMed XML record into a Paper object.

        Args:
            record: PubMed record dictionary

        Returns:
            Paper object or None if parsing fails
        """
        try:
            # Extract basic information
            article = record.get("MedlineCitation", {}).get("Article", {})
            pubmed_id = record.get("MedlineCitation", {}).get("PMID", "")
            title = article.get("ArticleTitle", "")
            
            # Get authors and affiliations
            author_list = article.get("AuthorList", [])
            authors = []
            affiliations = []
            for author in author_list:
                if isinstance(author, dict):
                    # Get author name
                    lastname = author.get("LastName", "")
                    forename = author.get("ForeName", "")
                    if lastname and forename:
                        authors.append(f"{lastname} {forename}")
                    
                    # Get affiliations
                    author_affils = author.get("AffiliationInfo", [])
                    if isinstance(author_affils, list):
                        for affil in author_affils:
                            if isinstance(affil, dict):
                                affiliation = affil.get("Affiliation", "")
                                if affiliation:
                                    affiliations.append(affiliation)
            
            # Get abstract
            abstract_text = article.get("Abstract", {}).get("AbstractText", [""])
            if isinstance(abstract_text, list):
                abstract = " ".join(abstract_text)
            else:
                abstract = str(abstract_text)
            
            # Parse publication date
            pub_date = article.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
            year = pub_date.get("Year", "")
            month = pub_date.get("Month", "1")
            day = pub_date.get("Day", "1")
            
            try:
                publication_date = datetime(int(year), int(month), int(day))
            except (ValueError, TypeError):
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

    def to_dataframe(self, papers: List[Paper]) -> 'pd.DataFrame':
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
                'Corresponding Author Email': paper.corresponding_author_email or ''
            })
        
        return pd.DataFrame(data) 