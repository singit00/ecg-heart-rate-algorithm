import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from src.heart_rate import (
    calculate_heart_rate,
    calculate_rr_intervals
)


def test_heart_rate_for_one_second_rr_interval():
    """
    Verify that an RR interval of one second corresponds
    to a heart rate of 60 BPM.
    """
    # Arrange: Define a known RR interval
    rr_intervals = np.array([1.0])

    # Act: Calculate the corresponding heart rate
    heart_rate = calculate_heart_rate(
        rr_intervals
    )

    # Assert: 1 second RR interval must result in 60 BPM
    assert heart_rate[0] == 60.0

def test_heart_rate_for_800ms_rr_interval():
    """
    Verify that an RR interval of 0.8 seconds corresponds
    to a heart rate of 75 BPM.
    """

    # Arrange
    rr_intervals = np.array([0.8])

    # Act
    heart_rate = calculate_heart_rate(rr_intervals)

    # Assert
    assert heart_rate[0] == 75.0

def test_multiple_rr_intervals():
    """
    Verify heart-rate calculation for multiple RR intervals.
    """

    # Arrange
    rr_intervals = np.array([
        1.0,
        0.8,
        0.6
    ])

    expected = np.array([
        60.0,
        75.0,
        100.0
    ])

    # Act
    heart_rate = calculate_heart_rate(rr_intervals)

    # Assert
    np.testing.assert_allclose(
        heart_rate,
        expected
    )

def test_rr_interval_calculation():
    """
    Verify conversion of R-peak sample distances
    into RR intervals in seconds.
    """

    # Arrange
    fs = 360

    r_peaks = np.array([
        0,
        360,
        720
    ])

    expected = np.array([
        1.0,
        1.0
    ])

    # Act
    rr_intervals = calculate_rr_intervals(
        r_peaks,
        fs
    )

    # Assert
    np.testing.assert_allclose(
        rr_intervals,
        expected
    )