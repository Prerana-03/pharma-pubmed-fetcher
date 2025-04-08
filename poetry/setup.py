from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pharma-pubmed-fetcher",
    version="0.1.0",
    author="PubMed Fetcher Team",
    author_email="your.email@example.com",
    description="A Python package to fetch research papers from PubMed based on user-defined queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pubmed-fetcher",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "biopython>=1.81",
        "click>=8.1.3",
        "pandas>=2.0.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "get-papers-list=pubmed_fetcher.main:main",
        ],
    },
) 