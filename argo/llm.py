from langchain_community.llms import Ollama
from typing import List, Dict
from config import config
import logging

logger = logging.getLogger(__name__)

class SafeOllama:
    def __init__(self):
        self.client = Ollama(
            model=config.MODEL_NAME,
            server_url=config.OLLAMA_URL,
            temperature=0.3,
            num_ctx=2048,
            num_gpu=0,  # Force CPU-only
            num_thread=4
        )
        self.max_retries = 3

    def generate(self, prompt: str, system_msg: str = "") -> str:
        messages = [{"role": "user", "content": prompt}]
        if system_msg:
            messages.insert(0, {"role": "system", "content": system_msg})

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat(messages)
                return response['message']['content']
            except Exception as e:
                logger.warning(f"LLM attempt {attempt+1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    return "Model response unavailable - try again later"
                
llm = SafeOllama()