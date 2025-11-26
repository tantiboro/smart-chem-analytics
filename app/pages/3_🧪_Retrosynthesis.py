import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.chemometrics.retrosynth import decompose_drug

st.set_page_config(page_title="Retrosynthesis", page_icon="🧪", layout="wide")

st.title("🧪 AI-Assisted Retrosynthesis")
st.markdown("### Deconstruct Target Molecules into Commercial Building Blocks")

# -----------------------------------------------------------------------------
# 1. INPUT
# -----------------------------------------------------------------------------
col1, col2 = st.columns([1, 2])
with col1:
    # Default is Ibuprofen
    target_smiles = st.text_area("Enter Target SMILES", value="CC(C)CC1=CC=C(C=C1)C(C)C(=O)O")
    run_btn = st.button("🔍 Propose Pathway", type="primary")
    
    st.info("""
    **How it works:**
    This tool uses the **RDKit BRICS algorithm** to identify chemically viable disconnection points (e.g., Amide, Ester, Carbon-Carbon bonds).
    """)

# -----------------------------------------------------------------------------
# 2. RESULTS
# -----------------------------------------------------------------------------
if run_btn and target_smiles:
    with st.spinner("Analyzing chemical structure..."):
        target_img, fragments = decompose_drug(target_smiles)
        
    if target_img:
        with col2:
            st.subheader("Target Molecule")
            st.image(f"data:image/png;base64,{target_img}")
            
        st.divider()
        st.subheader("proposed Disconnection (Step 1)")
        st.caption("Identified Precursors / Building Blocks:")
        
        # Display fragments in a grid
        cols = st.columns(len(fragments) if len(fragments) > 0 else 1)
        if len(fragments) > 0:
            for i, frag_img in enumerate(fragments):
                with cols[i]:
                    st.image(f"data:image/png;base64,{frag_img}")
                    st.markdown(f"**Precursor {i+1}**")
        else:
            st.warning("No clear retrosynthetic cuts found (Molecule might be too simple).")
            
    else:
        st.error("Invalid SMILES string.")
