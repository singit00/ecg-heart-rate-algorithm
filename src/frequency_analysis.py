import numpy as np


def calculate_fft(signal, fs):
    """
    Calculate the frequency spectrum of an ECG signal using the FFT.

    Parameters
    ----------
    signal : numpy.ndarray
        ECG signal samples in the time domain.
    fs : float
        Sampling frequency of the ECG signal in Hz.

    Returns
    -------
    frequencies : numpy.ndarray
        Frequency bins of the calculated spectrum in Hz.
    magnitude : numpy.ndarray
        Normalized magnitude spectrum of the ECG signal.
    """

    # Remove the mean value to suppress the DC component at 0 Hz
    signal = signal - np.mean(signal)

    # Determine the number of samples in the input signal
    n = len(signal)

    # Compute the one-dimensional FFT for a real-valued ECG signal.
    # rfft returns only the non-negative frequency components.
    fft_values = np.fft.rfft(signal)

    # Generate the corresponding frequency axis based on the
    # sampling frequency and the number of samples
    frequencies = np.fft.rfftfreq(
        n,
        d=1/fs
    )

    # Calculate and normalize the magnitude of the frequency spectrum
    magnitude = np.abs(fft_values)/n

    return frequencies, magnitude