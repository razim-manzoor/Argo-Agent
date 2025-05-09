from langchain.agents import Tool, initialize_agent
from argo.retrieval import retrieve_papers
from argo.vectorstore import VectorStore
from argo.llm import llm, summarize, generate_hypotheses
from pdfplumber import open as open_pdf

vectorstore = VectorStore()

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract full text from a PDF file."""
    text = []
    with open_pdf(pdf_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def prepare_documents(papers: list[dict]) -> list[dict]:
    """Download, extract, and structure docs for indexing."""
    docs = []
    for p in papers:
        content = extract_text_from_pdf(p["pdf_path"])
        docs.append({
            "id": p["id"],
            "text": content,
            "metadata": {"title": p["title"], "abstract": p["abstract"]}
        })
    return docs

# Define LangChain Tools
tools = [
    Tool(
        name="RetrievePapers",
        func=lambda q: retrieve_papers(q, max_results=5),
        description="Fetch latest papers from arXiv for a given topic"
    ),
    Tool(
        name="IndexPapers",
        func=lambda papers: vectorstore.index(prepare_documents(papers)),
        description="Index downloaded papers into the vector store"
    ),
    Tool(
        name="SearchPapers",
        func=lambda query: vectorstore.search(query, n_results=3),
        description="Perform semantic search on indexed papers"
    ),
    Tool(
        name="Summarize",
        func=lambda txt: summarize(txt),
        description="Summarize research text"
    ),
    Tool(
        name="Hypothesize",
        func=lambda summ: generate_hypotheses(summ),
        description="Generate novel research hypotheses"
    ),
]

# Initialize the agent with zero-shot React description
agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
)

def run_research_agent(topic: str) -> str:
    """Execute a full research workflow end-to-end."""
    return agent.run(f"Research topic: {topic}")