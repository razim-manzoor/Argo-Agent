from langchain_ollama import Ollama
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env for OLLAMA_SERVER_URL if specified

OLLAMA_SERVER = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434")

# Instantiate an OpenAI-compatible LLM client pointing to Ollama
llm = Ollama(model="llama2", server_url=OLLAMA_SERVER)

def summarize(text: str) -> str:
    """Generate a concise summary via the local LLM."""
    prompt = f"Please provide a concise summary:\n\n{text}"
    response = llm.chat([{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def generate_hypotheses(summary: str) -> str:
    """Produce three novel research hypotheses."""
    prompt = (
        f"Based on this summary, propose three novel research hypotheses, each "
        f"numbered: \n\n{summary}"
    )
    response = llm.chat([{"role": "user", "content": prompt}])
    return response.choices[0].message.content