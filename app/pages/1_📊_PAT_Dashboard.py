import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.decomposition import PCA
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.chemometrics.preprocess import preprocess_spectra

st.set_page_config(page_title="PAT Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/spectra/simulated_tablets.csv')
        spectral_cols = [c for c in df.columns if c.startswith('wl_')]
        X = df[spectral_cols].values
        wavelengths = [float(c.split('_')[1]) for c in spectral_cols]
        y = df['target_purity'].values
        return X, y, wavelengths
    except FileNotFoundError:
        return None, None, None

X, y, wl = load_data()

if X is not None:
    st.sidebar.header("🛠️ Preprocessing")
    use_sg = st.sidebar.checkbox("Apply Smoothing", value=True)
    sg_deriv = st.sidebar.selectbox("Derivative", [0, 1, 2], index=1)
    
    X_proc, _ = preprocess_spectra(X, sg_smooth=use_sg, sg_deriv=sg_deriv)

    st.title("📊 PAT Spectral Monitor")
    plot_df = pd.DataFrame(X_proc[:20].T, index=wl).reset_index()
    plot_df.columns = ['Wavelength'] + [f'S{i}' for i in range(20)]
    plot_df = plot_df.melt('Wavelength', var_name='Sample', value_name='Absorbance')
    
    chart = alt.Chart(plot_df).mark_line(opacity=0.5).encode(
        x='Wavelength', y='Absorbance', color=alt.value("#00AAFF"), detail='Sample'
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

    pca = PCA(n_components=2)
    scores = pca.fit_transform(X_proc)
    pca_df = pd.DataFrame(scores, columns=['PC1', 'PC2'])
    pca_df['Purity'] = y
    
    st.markdown("### Batch Uniformity (PCA)")
    pca_chart = alt.Chart(pca_df).mark_circle(size=60).encode(
        x='PC1', y='PC2', color=alt.Color('Purity', scale=alt.Scale(scheme='viridis')),
        tooltip=['Purity']
    ).interactive()
    st.altair_chart(pca_chart, use_container_width=True)
else:
    st.error("Data not found.")
