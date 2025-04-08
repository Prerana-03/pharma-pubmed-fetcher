import csv
import re
from typing import List
from Bio import Entrez

def search_pubmed(query: str, max_results: int, email: str) -> List[str]:
    Entrez.email = email
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_article_details(paper_ids: List[str], email: str, verbose: bool = False) -> List[dict]:
    Entrez.email = email
    handle = Entrez.efetch(db="pubmed", id=",".join(paper_ids), rettype="medline", retmode="text")
    records = handle.read()
    handle.close()

    papers = []
    entries = records.strip().split("\n\n")
    for entry in entries:
        paper = {}
        lines = entry.split("\n")
        for line in lines:
            if line.startswith("TI  -"):
                paper["Title"] = line[6:]
            elif line.startswith("AU  -"):
                if "Authors" not in paper:
                    paper["Authors"] = []
                paper["Authors"].append(line[6:])
            elif line.startswith("AD  -"):
                paper["Affiliation"] = line[6:]
            elif line.startswith("DP  -"):
                paper["Date"] = line[6:]
        if verbose:
            print(f"[DEBUG] Parsed: {paper.get('Title', 'No Title')}")

        # Filtering: company affiliation
            papers.append(paper)
    return papers

      
    if verbose:
        print(f"[DEBUG] Affiliation: {paper.get('Affiliation', 'N/A')}")
    papers.append(paper)


def save_results_to_csv(papers: List[dict], output_file: str):
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Title", "Authors", "Affiliation", "Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for paper in papers:
            writer.writerow({
                "Title": paper.get("Title", "Not Available"),
                "Authors": "; ".join(paper.get("Authors", [])),
                "Affiliation": paper.get("Affiliation", "Not Available"),
                "Date": paper.get("Date", "Not Available")
            })
