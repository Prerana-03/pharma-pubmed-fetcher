# pubmed_fetcher/utils.py

import re
from typing import Optional

def extract_email(text: str) -> Optional[str]:
    """Extracts first email from a string."""
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group(0) if match else None

def is_non_academic(affiliation: str) -> bool:
    """Heuristic to check if an affiliation is non-academic (pharma/biotech)."""
    affiliation_lower = affiliation.lower()
    pharma_keywords = ['pharma', 'biotech', 'therapeutics', 'labs', 'inc.', 'corp', 'gmbh', 'pvt ltd']
    university_keywords = ['university', 'college', 'institute', 'hospital', 'school', 'faculty']

    return (
        any(kw in affiliation_lower for kw in pharma_keywords)
        and not any(kw in affiliation_lower for kw in university_keywords)
    )
