import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from src.filtering import bandpass_filter


def test_bandpass_filter_preserves_in_band_frequency():
    """
    Verify that a frequency inside the passband is preserved
    with significantly higher amplitude than out-of-band frequencies.
    """

    # Arrange
    fs = 360
    duration = 10

    time = np.arange(0, duration, 1 / fs)

    low_frequency = np.sin(2 * np.pi * 0.2 * time)
    passband_frequency = np.sin(2 * np.pi * 10.0 * time)
    high_frequency = np.sin(2 * np.pi * 80.0 * time)

    test_signal = (
        low_frequency
        + passband_frequency
        + high_frequency
    )

    # Act
    filtered_signal = bandpass_filter(
        test_signal,
        fs,
    )

    # Assert
    frequencies = np.fft.rfftfreq(
        len(filtered_signal),
        d=1 / fs
    )

    spectrum = np.abs(
        np.fft.rfft(filtered_signal)
    )

    low_index = np.argmin(
        np.abs(frequencies - 0.2)
    )

    passband_index = np.argmin(
        np.abs(frequencies - 10.0)
    )

    high_index = np.argmin(
        np.abs(frequencies - 80.0)
    )

    low_amplitude = spectrum[low_index]
    passband_amplitude = spectrum[passband_index]
    high_amplitude = spectrum[high_index]

    assert passband_amplitude > low_amplitude
    assert passband_amplitude > high_amplitude