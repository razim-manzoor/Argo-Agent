import arxiv
import hashlib
from typing import List, Dict
from config import config
import datetime
import logging
import requests

logger = logging.getLogger(__name__)

class ArXivClient:
    @staticmethod
    def sanitize_entry(entry: arxiv.Result) -> Dict:
        return {
            "id": hashlib.sha256(entry.entry_id.encode()).hexdigest()[:32],
            "title": entry.title,
            "abstract": entry.summary,
            "published": entry.published.isoformat(),
            "authors": [a.name for a in entry.authors],
            "pdf_url": entry.pdf_url
        }

    @staticmethod
    def search(query: str, max_results: int = config.MAX_PAPERS) -> List[Dict]:
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            results = list(search.results())  # Convert generator to list
            return [ArXivClient.sanitize_entry(r) for r in results]
        except Exception as e:
            logger.error(f"ArXiv search failed: {str(e)}")
            return []

    @staticmethod
    def download_pdf(url: str, save_path: str) -> bool:
        try:
            response = requests.get(url, timeout=10)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            logger.error(f"PDF download failed: {str(e)}")
            return False