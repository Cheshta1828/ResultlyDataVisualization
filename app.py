import streamlit as st
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.markdown("<h1 style='text-align: center; color: black;'>Data Visualization</h1>", unsafe_allow_html=True)

col1 , col2 , col3 = st.columns(3)

with col1:
    st.header("Fetch data")
    option = st.selectbox(
    "Selected an already available result:",
    ("Fetch", "These", "With api"))
with col2:
    st.write("")
with col3:
    st.header("Upload data")
    st.download_button("Download exmaple result",data="data",file_name="example.csv",mime="text/csv",key=None)
    st.file_uploader("Upload custom result", label_visibility="visible")


