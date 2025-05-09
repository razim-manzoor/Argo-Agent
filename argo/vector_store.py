import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
from config import config
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.EMBEDDING_MODEL
        )
        
        self.collection = self.client.get_or_create_collection(
            name="research_papers",
            embedding_function=self.ef
        )

    def index_document(self, doc: Dict) -> None:
        try:
            self.collection.add(
                documents=[doc["text"]],
                metadatas=[doc["metadata"]],
                ids=[doc["id"]]
            )
        except Exception as e:
            logger.error(f"Indexing error: {str(e)}")

    def semantic_search(self, query: str, n_results: int = 3) -> List[Dict]:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            return [
                {"text": doc, "metadata": meta, "score": float(score)}
                for doc, meta, score in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []