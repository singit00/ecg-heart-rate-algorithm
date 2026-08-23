import wfdb
import numpy as np


#def load_reference_annotations(record_name):

#    annotation = wfdb.rdann(
#        f"data/{record_name}",
#        "atr"
#    )

#    return annotation.sample, annotation.symbol


# Annotation symbols considered as valid heart beats
# for the current MIT-BIH Record 100 evaluation
BEAT_SYMBOLS = {
    "N",
    "A",
}


def load_reference_beats(record_name):
    """
    Load reference beat annotations from the MIT-BIH dataset.

    Only annotation symbols representing relevant heart beats
    are retained for comparison with the detected R-peaks.

    Parameters
    ----------
    record_name : str
        Name of the ECG record, e.g. "100".

    Returns
    -------
    reference_beats : numpy.ndarray
        Sample indices of the reference heart beats.
    """

    # Load the expert reference annotations associated
    # with the selected ECG record
    annotation = wfdb.rdann(
        f"data/{record_name}",
        "atr"
    )

    reference_beats = []

    # Iterate over annotation positions and their corresponding symbols
    for sample, symbol in zip(
        annotation.sample,
        annotation.symbol
    ):
        # Keep only annotations classified as relevant heart beats
        if symbol in BEAT_SYMBOLS:
            reference_beats.append(sample)

    return  np.array(reference_beats)

def evaluate_detection(
    detected_peaks,
    reference_peaks,
    fs,
    tolerance_ms=50
):
    """
    Compare detected R-peaks with reference annotations.

    A detected peak is considered a true positive when a reference
    beat exists within the specified temporal tolerance window.

    Parameters
    ----------
    detected_peaks : numpy.ndarray
        Sample indices of detected R-peaks.
    reference_peaks : numpy.ndarray
        Sample indices of reference heart beats.
    fs : float
        Sampling frequency in Hz.
    tolerance_ms : float
        Maximum timing difference allowed for a valid match
        in milliseconds.

    Returns
    -------
    true_positives : int
        Number of correctly detected beats.
    false_positives : int
        Number of detected peaks without a matching reference beat.
    false_negatives : int
        Number of reference beats that were not detected.
    timing_errors : numpy.ndarray
        Timing differences between matched detected and reference peaks.
    false_positive_peaks : numpy.ndarray
        Sample positions of false-positive detections.
    """

    # Convert the matching tolerance from milliseconds to samples
    tolerance_samples = int(
         tolerance_ms / 1000 * fs #config["validation"]["tolerance_ms"] / 1000 * fs
    )

    # Store already matched reference beats to prevent
    # multiple detections from being assigned to the same beat
    matched_reference = set()

    true_positives = 0
    false_positives = 0

    # Store timing errors for correctly matched peaks
    timing_errors = []

    # Store false-positive locations for subsequent error analysis
    false_positive_peaks = []

    for detected in detected_peaks:

        # Store timing errors for correctly matched peaks
        distances = np.abs(
            reference_peaks - detected
        )

        # Identify the closest reference beat
        closest_index = np.argmin(distances)

        # Accept the detection when it lies inside the tolerance
        # window and the reference beat has not been matched before
        if (
            distances[closest_index] <= tolerance_samples
            and closest_index not in matched_reference
        ):
            # Mark the reference beat as matched
            true_positives += 1

            matched_reference.add(
                closest_index
            )

            # Calculate the signed timing error in samples
            error = (
                detected
                - reference_peaks[closest_index]
            )

            timing_errors.append(error)
            #false_positive_peaks.append(detected)

        else:

            # A detection without a valid reference match
            # is classified as a false positive
            false_positives += 1
            false_positive_peaks.append(detected)

    false_negatives = (
        len(reference_peaks)
        - len(matched_reference)
    )

    return (
        true_positives,
        false_positives,
        false_negatives,
        np.array(timing_errors),
        np.array(false_positive_peaks)
    )


def calculate_metrics(tp, fp, fn):
    """
    Calculate performance metrics for the R-peak detector.

    Parameters
    ----------
    tp : int
        Number of true-positive detections.
    fp : int
        Number of false-positive detections.
    fn : int
        Number of false-negative detections.

    Returns
    -------
    sensitivity : float
        Fraction of reference beats correctly detected.
    ppv : float
        Fraction of detected peaks that correspond to reference beats.
    """

    # Sensitivity describes how many reference beats
    # were successfully detected by the algorithm
    sensitivity = tp / (tp + fn)

    # Positive Predictive Value (PPV) describes how many
    # algorithm detections correspond to actual reference beats
    ppv = tp / (tp + fp)

    return sensitivity, ppv