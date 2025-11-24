import numpy as np
from scipy.signal import savgol_filter
from typing import Tuple, Dict, Optional, Literal

def snv(x: np.ndarray) -> np.ndarray:
    mean = np.mean(x, axis=1, keepdims=True)
    std = np.std(x, axis=1, keepdims=True)
    return (x - mean) / (std + 1e-12)

def preprocess_spectra(
    X: np.ndarray,
    sg_smooth: bool = True,
    sg_window: int = 15,
    sg_polyorder: int = 2,
    sg_deriv: int = 1,
    scatter_type: Literal['snv', 'msc', None] = 'snv',
    mean_center: bool = True,
) -> Tuple[np.ndarray, Dict]:
    X_proc = X.copy().astype(float)
    info: Dict = {}
    
    if sg_smooth:
        window = sg_window
        if window >= X_proc.shape[1]: window = X_proc.shape[1] - 1
        if window % 2 == 0: window += 1
        X_proc = savgol_filter(X_proc, window_length=window, polyorder=sg_polyorder, deriv=sg_deriv, axis=1)

    if scatter_type == 'snv':
        X_proc = snv(X_proc)

    if mean_center:
        mean_vec = np.mean(X_proc, axis=0)
        X_proc = X_proc - mean_vec
        info["mean_vec"] = mean_vec

    return X_proc, info
