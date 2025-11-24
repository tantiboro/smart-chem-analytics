import numpy as np
import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.chemometrics.preprocess import snv

def test_snv_normalization():
    """Test that SNV results in mean=0 and std=1"""
    # Create fake data: 5 samples, 10 wavelengths
    X = np.random.rand(5, 10)
    
    X_snv = snv(X)
    
    # Check mean is approx 0
    assert np.allclose(np.mean(X_snv, axis=1), 0, atol=1e-7)
    
    # Check std is approx 1
    assert np.allclose(np.std(X_snv, axis=1), 1, atol=1e-7)

if __name__ == "__main__":
    test_snv_normalization()
    print("✅ SNV Test Passed")
