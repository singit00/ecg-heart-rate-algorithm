import wfdb

def load_ecg(record_name):
    """
    Load a locally stored ECG record.

    Parameters
    ----------
    record_name : str
        Name of the ECG record to be loaded (e.g. "100").

    Returns
    -------
    ecg : numpy.ndarray
        ECG samples from the first signal channel.
    fs : float
        Sampling frequency of the ECG signal in Hz.
    """
    # Load the ECG record from the local data directory
    record = wfdb.rdrecord(
        f"data/{record_name}"
    )

    # Extract the first ECG signal channel
    ecg = record.p_signal[:, 0]

    # Read the sampling frequency from the record metadata
    fs = record.fs

    return ecg, fs