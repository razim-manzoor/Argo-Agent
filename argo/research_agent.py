from langchain.agents import Tool, initialize_agent
from typing import Callable, List
from config import config
from llm import llm
import logging
import os

logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        self.tools = self._create_tools()
        self.agent = initialize_agent(
            self.tools,
            llm,  # Use wrapped instance
            agent="zero-shot-react-description",
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )

    def _create_tools(self) -> List[Tool]:
        return [
            Tool(
                name="arxiv_search",
                func=self.arxiv_search,
                description="Search arXiv for scientific papers"
            ),
            Tool(
                name="semantic_search",
                func=self.semantic_search,
                description="Search indexed papers using semantic similarity"
            ),
            Tool(
                name="summarize_text",
                func=self.summarize_text,
                description="Generate concise summary of research text"
            ),
            Tool(
                name="generate_hypotheses",
                func=self.generate_hypotheses,
                description="Create research hypotheses from summaries"
            )
        ]

    @staticmethod
    def arxiv_search(query: str) -> str:
        from arxiv_client import ArXivClient
        from vector_store import VectorStore
        results = ArXivClient.search(query)
        
        # Index papers
        store = VectorStore()
        for paper in results:
            store.index_document({
                "id": paper["id"],
                "text": f"{paper['title']}\n{paper['abstract']}",
                "metadata": paper
            })
            
        return f"Found {len(results)} papers: " + "\n".join(
            [f"- {p['title']} ({p['published'][:4]})" for p in results]
        )

    @staticmethod
    def semantic_search(query: str) -> str:
        from vector_store import VectorStore
        results = VectorStore().semantic_search(query)
        return "\n".join([f"{r['metadata']['title']} (score: {r['score']:.2f})" for r in results])

    @staticmethod
    def summarize_text(text: str) -> str:
        return llm.generate(
            f"Create a 3-bullet summary of this research content:\n{text[:8000]}"
        )

    @staticmethod
    def generate_hypotheses(summary: str) -> str:
        return llm.generate(
            f"Based on this summary, suggest 2 research hypotheses:\n{summary}"
        )

    def run(self, query: str) -> str:
        try:
            return self.agent.run(
                f"You are a research assistant. Break down this task: {query}"
                "\nUse available tools and keep responses concise."
            )
        except Exception as e:
            logger.error(f"Agent failed: {str(e)}")
            return "Research process failed - please try a simpler query"