import streamlit as st

from feature_3_stats.stats_feature import show_stats_page

st.set_page_config(
    page_title="GeneVault",
    layout="wide"
)

st.sidebar.title("🧬 GeneVault")

st.sidebar.markdown("---")

st.sidebar.info("""
Population Analytics Module
""")
show_stats_page()