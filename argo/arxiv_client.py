import arxiv
import hashlib
from typing import List, Dict
from config import config
import datetime
import logging

logger = logging.getLogger(__name__)

class ArXivClient:
    @staticmethod
    def sanitize_entry(entry: arxiv.Result) -> Dict:
        return {
            "id": hashlib.md5(entry.entry_id.encode()).hexdigest(),
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
            return [ArXivClient.sanitize_entry(r) for r in search.results()]
        except Exception as e:
            logger.error(f"ArXiv search failed: {str(e)}")
            return []