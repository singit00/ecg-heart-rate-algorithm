from scipy.signal import find_peaks


def detect_r_peaks(
    signal,
    fs,
    min_distance_seconds=0.5,
    prominence=0.5
):
#def detect_r_peaks(signal, fs, config):

    """
    Detect R-peaks in a filtered ECG signal.

    Parameters
    ----------
    signal : numpy.ndarray
        Filtered ECG signal.

    fs : float
        Sampling frequency in Hz.

    min_distance_seconds : float
        Minimum allowed time distance between two R-peaks
        in seconds.

    prominence : float
        Minimum prominence required for a peak.

    Returns
    -------
    peaks : numpy.ndarray
        Sample indices of detected R-peaks.
    """

    # Define the minimum physiologically plausible time distance
    # between two detected R-peaks
    # min_distance_seconds = int(min_distance_seconds * fs)

    # Convert the minimum peak distance from seconds to samples
    min_distance_samples = int(
        min_distance_seconds * fs
    )

    # Detect prominent peaks in the filtered ECG signal.
    # The distance criterion prevents multiple detections within
    # the same QRS complex.
    peaks, _ = find_peaks(
        signal,
        distance=min_distance_samples,
        prominence=prominence  #prominence = config["peak_detection"]["prominence"]
    )

    return peaks