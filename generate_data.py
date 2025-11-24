import numpy as np
import pandas as pd
import os

def generate_synthetic_spectra(n_samples=100, n_features=200):
    np.random.seed(42)
    wavelengths = np.linspace(900, 1700, n_features)
    slopes = np.random.normal(0, 0.01, n_samples)
    offsets = np.random.normal(0.5, 0.1, n_samples)
    X = np.zeros((n_samples, n_features))
    peaks = [(1100, 50, 0.2), (1400, 40, 0.3), (1600, 30, 0.15)]
    
    for i in range(n_samples):
        spectrum = offsets[i] + slopes[i] * np.linspace(0, 10, n_features)
        concentration = np.random.uniform(0.8, 1.2)
        for center, width, height in peaks:
            idx = np.abs(wavelengths - center).argmin()
            x_range = np.arange(n_features)
            spectrum += (height * concentration) * np.exp(-0.5 * ((x_range - idx) / (width/10))**2)
        spectrum += np.random.normal(0, 0.002, n_features)
        X[i, :] = spectrum

    y_purity = np.mean(X[:, 50:150], axis=1) * 100 
    y_purity = (y_purity - y_purity.min()) / (y_purity.max() - y_purity.min()) * 10 + 90
    return X, y_purity, wavelengths

if __name__ == "__main__":
    X, y, wl = generate_synthetic_spectra()
    df = pd.DataFrame(X, columns=[f"wl_{int(w)}" for w in wl])
    df['target_purity'] = y
    os.makedirs('data/spectra', exist_ok=True)
    df.to_csv('data/spectra/simulated_tablets.csv', index=False)
    print("✅ Saved to data/spectra/simulated_tablets.csv")
