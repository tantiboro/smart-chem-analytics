import streamlit as st
st.set_page_config(page_title="Smart Chem Analytics", page_icon="🧪", layout="wide")
st.title("🧪 Smart Pharma Analytics Platform")
st.info("👈 **Select 'PAT Dashboard' from the Sidebar to see the models.**")
st.subheader("System Status")
c1, c2 = st.columns(2)
c1.metric("API Status", "Online", delta="OK")
c2.metric("Data Source", "Simulated NIR", delta="Loaded")
