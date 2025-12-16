import streamlit as st


st.set_page_config(
   page_title="NBA Analytics Suite",
   page_icon="🏀",
   layout="wide"
)


st.title("🏀 NBA Analytics Suite")
st.markdown("""
Welcome! Use the sidebar to navigate between tools:


- **Rebuild Analyzer** – Historical rebuild detection 
- **Playoff Return Predictor** – ML-based prediction tool
""")