import streamlit as st
from knowledge_weaver.indexer import MultiModalIndexer
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Knowledge Weaver", layout="wide")
st.title("Multi‑Modal Knowledge Weaver")

data_dir = st.text_input("Data directory", "data")
index_dir = st.text_input("Index directory", "index")
if st.button("Build index"):
    idx = MultiModalIndexer(index_dir=index_dir)
    with st.spinner("Indexing..."):
        idx.build(data_dir)
    st.success("Done.")

q = st.text_input("Query", "solar panels on rooftops")
k = st.slider("Top K", 1, 20, 5)
if st.button("Search"):
    idx = MultiModalIndexer(index_dir=index_dir)
    res = idx.search(q, k)
    st.write(pd.DataFrame(res))
