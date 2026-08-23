import numpy as np


def calculate_rr_intervals(r_peaks, fs):
    """
    Calculate RR intervals from detected R-peak positions.

    Parameters
    ----------
    r_peaks : numpy.ndarray
        Sample indices of detected R-peaks.
    fs : float
        Sampling frequency in Hz.

    Returns
    -------
    rr_intervals : numpy.ndarray
        Time intervals between consecutive R-peaks in seconds.
    """

    # Calculate the sample distance between consecutive R-peaks
    rr_samples = np.diff(r_peaks)

    # Convert the sample distances into time intervals in seconds
    rr_intervals = rr_samples / fs

    return rr_intervals


def calculate_heart_rate(rr_intervals):
    """
    Calculate the instantaneous heart rate from RR intervals.

    Parameters
    ----------
    rr_intervals : numpy.ndarray
        Time intervals between consecutive R-peaks in seconds.

    Returns
    -------
    heart_rate : numpy.ndarray
        Instantaneous heart rate values in beats per minute (BPM).
    """

    # Convert each RR interval into an instantaneous heart rate.
    # One minute contains 60 seconds, therefore HR = 60 / RR.
    heart_rate = 60.0 / rr_intervals

    return heart_rate