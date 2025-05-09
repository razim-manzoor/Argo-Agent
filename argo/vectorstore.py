import chromadb
from chromadb.utils import embedding_functions
from argo.embedding import Embedder

class VectorStore:
    def __init__(self, collection_name: str = "argo_papers"):
        self.client = chromadb.Client()
        if collection_name in [c.name for c in self.client.list_collections()]:
            self.collection = self.client.get_collection(collection_name)
        else:
            ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=Embedder().model
            )
            self.collection = self.client.create_collection(name=collection_name, embedding_function=ef)

    def index(self, docs: list[dict]):
        """Index list of {'id','text','metadata'} entries."""
        self.collection.add(
            documents=[d["text"] for d in docs],
            metadatas=[d["metadata"] for d in docs],
            ids=[d["id"] for d in docs]
        )

    def search(self, query: str, n_results: int = 3):
        """Semantic search for top-n matching documents."""
        return self.collection.query(query_texts=[query], n_results=n_results)