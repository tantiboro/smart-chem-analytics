# Smart Pharma Analytics Platform 🧪

A Cloud-Native Chemometrics & Sustainability dashboard designed for Pharmaceutical Manufacturing (PAT).

## 🚀 Live Demo
**[Click Here to Open the App](https://smart-chem-app-g66s7v5f6a-uc.a.run.app)**
*(Hosted on Google Cloud Run)*

## 🎯 Project Goals
This platform bridges the gap between **Analytical Chemistry** and **Data Engineering** by providing:
1.  **Real-Time PAT Monitoring:** Spectral preprocessing (Savitzky-Golay, SNV) and Batch Anomaly Detection (PCA).
2.  **Sustainability Modeling:** A simulator for Carbon Intensity (Scope 1, 2 & 3) in API manufacturing.
3.  **Serverless Infrastructure:** Deployed using Docker containers on Google Cloud.

## 🏗️ Architecture
* **Frontend:** Streamlit (Python)
* **Scientific Compute:** `scikit-learn`, `scipy` (Signal Processing), `numpy`
* **Containerization:** Docker (Multi-stage build)
* **Cloud Provider:** Google Cloud Platform (Cloud Run)

## 📂 Key Directories
* `src/chemometrics`: Core algorithms for spectral data processing.
* `app/pages`: Modular dashboard views (PAT & Carbon Footprint).
* `infra/`: Terraform definitions (IaC).
* `tests/`: Unit tests for data validation.

## 🛠️ Local Setup
```bash
# 1. Install Dependencies
pip install -r requirements.txt

# 2. Generate Synthetic Data
python generate_data.py

# 3. Run the App
streamlit run app/main.py
