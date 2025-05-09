from langchain_community.llms import Ollama
from typing import List, Dict
from argo.config import config
import logging
import os
from dotenv import load_dotenv 

load_dotenv()

logger = logging.getLogger(__name__)  

class SafeOllama:
    def __init__(self):
        self.client = Ollama(
            model=os.getenv("OLLAMA_MODEL", "tinyllama"),
            base_url=os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434"),
            temperature=0.3,
            num_ctx=2048,
            # num_gpu=0,  
        )
        self.max_retries = 3

    def generate(self, prompt: str, system_msg: str = "") -> str:
        """Generate text using the Ollama model with proper error handling"""
        messages = []
        if system_msg:
            messages.append({"role": "system", "content": system_msg})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(self.max_retries):
            try:
                # Use invoke() instead of chat()
                response = self.client.invoke(
                    "\n".join([f"{m['role']}: {m['content']}" for m in messages])
                )
                return response
            except Exception as e:
                logger.warning(f"LLM attempt {attempt+1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    logger.error("Max retries exceeded")
                    return "Model response unavailable - try again later"
        return ""  # Fallback return

llm = SafeOllama()