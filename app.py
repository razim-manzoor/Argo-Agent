import streamlit as st
from argo.research_agent import ResearchAgent
from argo.config import config
import time
import logging

logging.basicConfig(level=logging.INFO)

def main():
    st.set_page_config(page_title="Argo Lite", layout="centered")
    st.title("🦥 Argo Lite - Low-Memory Research Assistant")
    
    with st.sidebar:
        st.header("Settings")
        config.MAX_PAPERS = st.slider("Max Papers", 1, 5, 2)
        st.caption("Adjust based on system memory (8GB recommended ≤3 papers)")
    
    query = st.text_input("Research Topic", "recent advances in battery technology")
    
    if st.button("Start Research"):
        with st.status("Processing...", expanded=True) as status:
            agent = ResearchAgent()
            
            try:
                st.write("🔍 Searching arXiv...")
                start = time.perf_counter()
                
                result = agent.run(query)
                
                st.write("📊 Analyzing results...")
                time.sleep(0.5)  # Simulate processing
                
                duration = time.perf_counter() - start
                status.update(label=f"Completed in {duration:.1f}s", state="complete")
                
                with st.container(border=True):
                    st.markdown(result)
                    st.download_button(
                        label="Download Report",
                        data=result,
                        file_name="research_report.md",
                        mime="text/markdown"
                    )
                    
            except Exception as e:
                st.error(f"Research failed: {str(e)}")
                logging.error(f"App error: {str(e)}")

if __name__ == "__main__":
    main()