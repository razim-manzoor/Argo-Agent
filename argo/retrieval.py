import os
import arxiv
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path(__file__).parent.parent / "data" / "pdfs"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def retrieve_papers(query: str, max_results: int = 5) -> List[Dict]:
    """Search arXiv and download PDFs locally."""
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)
    papers = []
    for result in search.results():
        pdf_path = DATA_DIR / f"{result.entry_id.replace('/', '_')}.pdf"
        if not pdf_path.exists():
            result.download_pdf(filename=pdf_path)
        papers.append({
            "id": result.entry_id,
            "title": result.title,
            "abstract": result.summary,
            "pdf_path": str(pdf_path)
        })
    return papers