import streamlit as st
from argo.research_agent import ResearchAgent
from argo.config import config
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def format_report(response: str) -> str:
    sections = {
        "Hypotheses": ["- HYPOTHESIS:", "Hypotheses:"],
        "Summary": ["- SUMMARY:", "Summary:"],
        "References": ["- REFERENCES:", "References:"]
    }
    formatted = {}
    current_section = None
    
    for line in response.split('\n'):
        for section, keywords in sections.items():
            if any(line.startswith(kw) for kw in keywords):
                current_section = section
                formatted[current_section] = []
                line = line.replace(keywords[0], "").strip()
                break
                
        if current_section and line.strip():
            formatted[current_section].append(line)
    
    return formatted

def main():
    st.set_page_config(page_title="Argo Lite", layout="centered")
    st.title("🦥 Argo - Research Assistant")
    
    with st.sidebar:
        st.header("Settings")
        config.MAX_PAPERS = st.slider("Max Papers", 1, 5, 2)
        st.caption("Recommended ≤3 papers for optimal performance")
    
    query = st.text_input("Research Topic", "recent advances in battery technology")
    
    if st.button("Start Research"):
        with st.status("🚀 Starting research process...", expanded=True) as status:
            try:
                agent = ResearchAgent()
                start_time = time.perf_counter()
                
                # Progress updates
                st.write("🔍 Searching arXiv...")
                time.sleep(0.5)
                
                st.write("📥 Indexing papers...")
                time.sleep(0.3)
                
                st.write("🧠 Analyzing content...")
                result = agent.run(query)
                
                # Formatting
                duration = time.perf_counter() - start_time
                formatted = format_report(result)
                
                status.update(
                    label=f"✅ Research completed in {duration:.1f}s",
                    state="complete",
                    expanded=False
                )
                
                # Display results
                with st.container():
                    if "Hypotheses" in formatted:
                        with st.expander("Generated Hypotheses", expanded=True):
                            st.markdown("\n".join(formatted["Hypotheses"]))
                    
                    if "Summary" in formatted:
                        with st.expander("Key Summary", expanded=False):
                            st.markdown("\n".join(formatted["Summary"]))
                    
                    # Download button
                    report_content = f"# Research Report\n\n{result}"
                    st.download_button(
                        label="📥 Download Full Report",
                        data=report_content,
                        file_name=f"research_report_{datetime.now().date()}.md",
                        mime="text/markdown"
                    )
                    
            except Exception as e:
                st.error(f"❌ Research failed: {str(e)}")
                logging.error(f"App error: {str(e)}")

if __name__ == "__main__":
    main()