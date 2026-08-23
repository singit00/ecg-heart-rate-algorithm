import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from src.filtering import bandpass_filter
from src.peak_detection import detect_r_peaks
from src.heart_rate import (
    calculate_rr_intervals,
    calculate_heart_rate
)


def test_complete_ecg_processing_pipeline():
    """
    Verify the complete ECG processing pipeline using a synthetic
    ECG-like signal with known R-peak positions.

    The test covers:
    filtering -> R-peak detection -> RR interval calculation
    -> heart rate calculation.
    """

    # Arrange
    fs = 360
    duration = 6

    number_of_samples = fs * duration
    time = np.arange(number_of_samples) / fs

    # Add a small low-frequency baseline variation
    signal = 0.05 * np.sin(
        2 * np.pi * 0.2 * time
    )

    # Define R-peaks at 2 s, 3 s and 4 s.
    # Keeping the peaks away from the signal boundaries reduces
    # filter edge effects during zero-phase filtering.
    expected_peaks = np.array([
        720,
        1080,
        1440
    ])

    # Width of the synthetic QRS complex in samples
    sigma_samples = 8

    sample_indices = np.arange(
        number_of_samples
    )

    # Generate smooth QRS-like pulses using Gaussian functions
    for peak in expected_peaks:

        qrs = 2.0 * np.exp(
            -0.5
            * (
                (sample_indices - peak)
                / sigma_samples
            ) ** 2
        )

        signal += qrs

    # Act
    filtered_signal = bandpass_filter(
        signal,
        fs
    )

    detected_peaks = detect_r_peaks(
        filtered_signal,
        fs
    )

    rr_intervals = calculate_rr_intervals(
        detected_peaks,
        fs
    )

    heart_rates = calculate_heart_rate(
        rr_intervals
    )

    # Assert
    assert len(detected_peaks) == 3

    # Allow a small timing tolerance because filtering and peak
    # detection may shift the detected maximum by a few samples
    np.testing.assert_allclose(
        detected_peaks,
        expected_peaks,
        atol=2
    )

    np.testing.assert_allclose(
        rr_intervals,
        np.array([
            1.0,
            1.0
        ]),
        atol=0.01
    )

    np.testing.assert_allclose(
        heart_rates,
        np.array([
            60.0,
            60.0
        ]),
        atol=1.0
    )