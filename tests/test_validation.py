import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from src.validation import (
    evaluate_detection,
    calculate_metrics
)


def test_validation_counts_tp_fp_fn_correctly():
    """
    Verify that true positives, false positives and
    false negatives are counted correctly.
    """

    # Arrange
    fs = 360

    reference_peaks = np.array([
        360,
        720,
        1080
    ])

    detected_peaks = np.array([
        360,   # TP
        720,   # TP
        900    # FP
    ])

    # Act
    tp, fp, fn, timing_errors, false_positive_peaks = evaluate_detection(
        detected_peaks,
        reference_peaks,
        fs
    )

    # Assert
    assert tp == 2
    assert fp == 1
    assert fn == 1

    np.testing.assert_array_equal(
        false_positive_peaks,
        np.array([900])
    )


def test_validation_metrics():
    """
    Verify sensitivity and PPV calculation.
    """

    # Arrange
    tp = 8
    fp = 2
    fn = 2

    # Act
    sensitivity, ppv = calculate_metrics(
        tp,
        fp,
        fn
    )

    # Assert
    assert sensitivity == 0.8
    assert ppv == 0.8