import numpy as np
from scipy.signal import savgol_filter
from typing import Tuple, Dict, Optional, Literal

def snv(x: np.ndarray) -> np.ndarray:
    """Standard Normal Variate (SNV): Normalizes each spectrum to mean=0, std=1."""
    mean = np.mean(x, axis=1, keepdims=True)
    std = np.std(x, axis=1, keepdims=True)
    return (x - mean) / (std + 1e-12)

def msc(x: np.ndarray, reference: Optional[np.ndarray] = None) -> np.ndarray:
    """Multiplicative Scatter Correction (MSC)."""
    # If no reference is provided, use the mean of the current batch
    if reference is None:
        reference = np.mean(x, axis=0)
    
    n_samples, n_features = x.shape
    x_msc = np.zeros_like(x)
    
    for i in range(n_samples):
        # Fit linear regression: sample = a * reference + b
        fit = np.polyfit(reference, x[i, :], 1, full=False)
        # Apply correction: (sample - intercept) / slope
        x_msc[i, :] = (x[i, :] - fit[1]) / fit[0]
        
    return x_msc

def preprocess_spectra(
    X: np.ndarray,
    sg_smooth: bool = True,
    sg_window: int = 15,
    sg_polyorder: int = 2,
    sg_deriv: int = 1,
    scatter_type: Literal['snv', 'msc', None] = 'snv',
    mean_center: bool = True,
) -> Tuple[np.ndarray, Dict]:
    """
    Full Chemometric Preprocessing Pipeline.
    Order: Smoothing -> Scatter Correction -> Mean Centering
    """
    X_proc = X.copy().astype(float)
    info: Dict = {}
    
    # 1. Savitzky-Golay (Smoothing & Derivatives)
    if sg_smooth:
        # Dynamic window sizing to prevent errors on small datasets
        window = sg_window
        if window >= X_proc.shape[1]: window = X_proc.shape[1] - 1
        if window % 2 == 0: window += 1
        
        X_proc = savgol_filter(X_proc, window_length=window, polyorder=sg_polyorder, deriv=sg_deriv, axis=1)

    # 2. Scatter Correction (SNV or MSC)
    if scatter_type == 'snv':
        X_proc = snv(X_proc)
    elif scatter_type == 'msc':
        X_proc = msc(X_proc)

    # 3. Mean Centering
    if mean_center:
        mean_vec = np.mean(X_proc, axis=0)
        X_proc = X_proc - mean_vec
        info["mean_vec"] = mean_vec

    return X_proc, info
