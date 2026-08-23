from scipy.signal import butter, filtfilt


def bandpass_filter(signal, fs, lowcut=0.5, highcut=40.0, order=4):
#def bandpass_filter(signal, fs, config):
    """
    Apply a Butterworth bandpass filter to an ECG signal.

    The filter suppresses low-frequency baseline variations and
    high-frequency noise while preserving the relevant ECG components.

    Parameters
    ----------
    signal : numpy.ndarray
        Input ECG signal.
    fs : float
        Sampling frequency in Hz.
    lowcut : float
        Lower cutoff frequency in Hz.
    highcut : float
        Upper cutoff frequency in Hz.
    order : int
        Order of the Butterworth filter.

    Returns
    -------
    filtered_signal : numpy.ndarray
        Bandpass-filtered ECG signal.
    """

    # Calculate the Nyquist frequency, which corresponds to half
    # of the sampling frequency
    nyquist = fs / 2

    # Normalize the cutoff frequencies with respect to the
    # Nyquist frequency for the digital filter design

    low = lowcut / nyquist #low = config["filter"]["lowcut_hz"] / nyquist
    high = highcut / nyquist #high = config["filter"]["highcut_hz"] / nyquist
    
    numerator , denominator  = butter(
        order, #config["filter"]["order"],
        [low, high],
        btype="band"
    )

    # Apply zero-phase filtering by processing the signal
    # forward and backward to avoid phase shifts of the ECG peaks
    filtered_signal = filtfilt(
        numerator,
        denominator,
        signal
    )

    return filtered_signal