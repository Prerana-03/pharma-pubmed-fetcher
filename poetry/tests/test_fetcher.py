from pubmed_fetcher.core import fetch_and_filter_papers
import os

def test_fetch_and_filter(tmp_path):
    output_file = tmp_path / "test_results.csv"
    fetch_and_filter_papers("cancer AND drug", 5, str(output_file), "your@email.com", verbose=False)

    assert os.path.exists(output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        contents = f.read()
        assert "Title" in contents
        assert "Affiliations" in contents
        assert len(contents.splitlines()) > 1

        # Optional: only check if result count > 0
        assert any(term in contents.lower() for term in ["pharma", "biotech"])
