import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_NAME = os.getenv("OLLAMA_MODEL", "tinyllama")
    OLLAMA_URL = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434")
    DATA_DIR = Path(__file__).parent.parent / "data"
    MAX_PAPERS = int(os.getenv("MAX_PAPERS", 3))
    MAX_TEXT_LENGTH = 250_000  # Characters per paper
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    CHROMA_DIR = DATA_DIR / "chromadb"
    
config = Config()