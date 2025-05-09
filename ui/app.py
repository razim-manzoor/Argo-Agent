import streamlit as st
from argo.agent import run_research_agent
from time import sleep

st.set_page_config(page_title="Argo Research Assistant", layout="wide")
st.title("🦜🔗 Argo: Autonomous Research Assistant")

with st.sidebar:
    st.header("Settings")
    max_results = st.slider("Max Papers to Retrieve", 1, 10, 5)
    st.info("Argo will fetch, index, summarize, and hypothesize automatically.")

topic = st.text_input("Enter Research Topic", value="graph neural networks")

if st.button("Run Agent"):    
    st.info(f"🌐 Fetching top {max_results} papers on '{topic}'...")
    placeholder = st.empty()

    # Simulate progress while running
    for i in range(4):
        placeholder.text(f"Step {i+1}/4 in progress...")
        sleep(0.5)

    with st.spinner("🚀 Argo is running..."):
        output = run_research_agent(topic)

    st.subheader("📝 Agent Output")
    st.code(output, language="markdown")

    st.subheader("👍 Feedback")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Refine Summary"):
            st.info("Argo will refine summaries based on your feedback.")
            # In a real app, trigger agent rerun with feedback loop
        if st.button("Expand Search"):
            st.info("Argo will fetch additional papers for deeper insights.")
            # trigger agent.run with increased max_results
    with col2:
        if st.button("Accept and Export"):
            st.success("Exporting results to PDF report…")
            # implement export logic

    placeholder.empty()