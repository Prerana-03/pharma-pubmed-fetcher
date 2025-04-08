import logging
from Bio import Entrez
import pandas as pd

def fetch_and_filter_papers(query, max_results, output, email, verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    Entrez.email = email

    logging.info(f"Searching PubMed for query: '{query}' with max {max_results} results")

    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
    except Exception as e:
        logging.error(f"Failed to search PubMed: {e}")
        return

    ids = record['IdList']
    logging.info(f"Found {len(ids)} articles.")

    results = []

    for id_ in ids:
        try:
            handle = Entrez.efetch(db="pubmed", id=id_, rettype="xml", retmode="text")
            paper = Entrez.read(handle)
            handle.close()

            article = paper['PubmedArticle'][0]
            title = article['MedlineCitation']['Article']['ArticleTitle']
            aff_texts = []

            authors = article['MedlineCitation']['Article'].get('AuthorList', [])
            for author in authors:
                if 'AffiliationInfo' in author:
                    for aff in author['AffiliationInfo']:
                        if 'Affiliation' in aff:
                            aff_texts.append(aff['Affiliation'])

            if any("pharma" in aff.lower() or "biotech" in aff.lower() for aff in aff_texts):
                results.append({
                    "Title": title,
                    "Affiliations": "; ".join(aff_texts)
                })

        except Exception as e:
            logging.warning(f"Error parsing article {id_}: {e}")

    df = pd.DataFrame(results)
    df.to_csv(output, index=False)
    logging.info(f"Saved {len(results)} filtered articles to '{output}'")
