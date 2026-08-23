import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from src.peak_detection import detect_r_peaks


def test_detect_r_peaks_at_known_positions():
    """
    Verify that R-peaks at known sample positions
    are detected correctly.
    """

    # Arrange: Define sampling frequency and signal duration
    fs = 360
    duration = 4

    number_of_samples = fs * duration

    # Create an artificial signal without background activity
    signal = np.zeros(number_of_samples)

    # Define known R-peak positions.
    # The peaks are separated by one second.
    expected_peaks = np.array([
        360,
        720,
        1080
    ])

    # Insert artificial R-peaks with sufficient amplitude
    signal[expected_peaks] = 1.0

    # Act: Run the R-peak detection algorithm
    detected_peaks = detect_r_peaks(
        signal,
        fs
    )

    # Assert: Detected positions must match the known positions
    np.testing.assert_array_equal(
        detected_peaks,
        expected_peaks
    )

def test_r_peaks_respect_minimum_distance():
    """
    Verify that peaks closer than the configured minimum
    distance are not detected as separate R-peaks.
    """

    # Arrange
    fs = 360

    signal = np.zeros(fs * 3)

    # First peak at 1.0 s
    first_peak = 360

    # Second peak only 0.2 s later
    second_peak = 432

    signal[first_peak] = 1.0
    signal[second_peak] = 0.8

    # Act
    detected_peaks = detect_r_peaks(
        signal,
        fs
    )

    # Assert: Only the dominant peak should remain
    assert len(detected_peaks) == 1

    assert detected_peaks[0] == first_peak