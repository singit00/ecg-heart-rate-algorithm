import matplotlib.pyplot as plt
import numpy as np

from src.load_ecg import load_ecg
from src.frequency_analysis import calculate_fft
from src.filtering import bandpass_filter
from src.peak_detection import detect_r_peaks
from src.validation import load_reference_beats

from src.heart_rate import (
    calculate_rr_intervals,
    calculate_heart_rate
)

from src.validation import (
    evaluate_detection,
    calculate_metrics
)

from tests.test_heart_rate import test_heart_rate_for_one_second_rr_interval
from config.read_json import read_json

# ============================================================
# CONFIGURATION
# ============================================================

config = read_json("config.json")


# ============================================================
# 1. ECG DATA ACQUISITION
# ============================================================

# Load the ECG signal and sampling frequency from Record 100
ecg, fs = load_ecg(config["record"])

print("Sampling frequency:", fs, "Hz")
print("Number of samples:", len(ecg))
print("Duration:", len(ecg) / fs, "seconds")

print("Minimum:", np.min(ecg))
print("Maximum:", np.max(ecg))
print("Mean:", np.mean(ecg))
print("Standard deviation:", np.std(ecg))


# ============================================================
# 2. SIGNAL PREPARATION
# ============================================================



if config["duration"] is not 0:
    #duration = 10
    samples = int(int(config["duration"]) * fs)

    ecg_segment = ecg[:samples]
    time = np.arange(samples) / fs
else:
    # Use the complete ECG record for algorithm evaluation
    ecg_segment = ecg

    # Generate the time axis based on the sampling frequency
    time = np.arange(len(ecg_segment)) / fs

filename = str(config["duration"])



plt.figure(figsize=(12, 4))
plt.plot(time, ecg_segment)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude [mV]")
plt.title("Raw ECG Signal")

plt.grid()
plt.savefig('C:\\git\\ecg-heart-rate-algorithm\\docs\\images\\raw_ecg_' +filename + '.png')

# Use the complete ECG record for algorithm evaluation
#ecg_segment = ecg

# Generate the time axis based on the sampling frequency
#time = np.arange(len(ecg_segment)) / fs

#plt.figure(figsize=(12, 4))
#plt.plot(time, ecg_segment)
#plt.xlabel("Time [s]")
#plt.ylabel("Amplitude [mV]")
#plt.title("Raw ECG Signal")

#plt.grid()
#plt.show()
#plt.savefig('C:\\git\\ecg-heart-rate-algorithm\\docs\\images\\raw_ecg.png')


# ============================================================
# 3. FREQUENCY-DOMAIN ANALYSIS
# ============================================================

# Transform the ECG signal into the frequency domain
# to inspect its spectral components
frequencies, magnitude = calculate_fft(
    ecg_segment,
    fs
)

plt.figure(figsize=(12, 4))
plt.plot(frequencies, magnitude)

plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.title("Frequency Spectrum of ECG")

plt.xlim(0, 50)
plt.grid()

#plt.show()
plt.savefig('C:\\git\\ecg-heart-rate-algorithm\\docs\\images\\ecg_frequency_spectrum_50.png')

plt.figure(figsize=(12, 4))
plt.plot(frequencies, magnitude)

plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.title("Frequency Spectrum of ECG")

plt.xlim(0, 100)
plt.grid()

#plt.show()
plt.savefig('C:\\git\\ecg-heart-rate-algorithm\\docs\\images\\ecg_frequency_spectrum_100.png')

plt.figure(figsize=(12, 4))
plt.plot(frequencies, magnitude)

plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.title("Frequency Spectrum of ECG")

plt.xlim(0, 180)
plt.grid()

#plt.show()
plt.savefig('C:\\git\\ecg-heart-rate-algorithm\\docs\\images\\ecg_frequency_spectrum_180.png')


# ============================================================
# 4. ECG BANDPASS FILTERING
# ============================================================

# Suppress baseline variations and high-frequency noise
# while preserving relevant ECG components
filtered_ecg = bandpass_filter(
    ecg_segment,
    fs,
    config
)

plt.figure(figsize=(12, 5))
plt.plot(
    time,
    ecg_segment,
    label="Raw ECG",
    alpha=0.6
)

plt.plot(
    time,
    filtered_ecg,
    label="Filtered ECG"
)

plt.xlabel("Time [s]")
plt.ylabel("Amplitude [mV]")
plt.title("Raw vs. Filtered ECG")

plt.legend()
plt.grid()

#plt.show()
plt.savefig('C:\\git\\ecg-heart-rate-algorithm\\docs\\images\\ecg_raw_vs_filtered_ecg.png')

# ============================================================
# 5. R-PEAK DETECTION
# ============================================================

# Detect the R-peaks used for subsequent RR interval calculation
r_peaks = detect_r_peaks(
    filtered_ecg,
    fs,
    config
)

print("Number of detected R-peaks:", len(r_peaks))

plt.figure(figsize=(12, 5))

plt.plot(
    time,
    filtered_ecg,
    label="Filtered ECG"
)

plt.plot(
    time[r_peaks],
    filtered_ecg[r_peaks],
    "rx",
    label="Detected R-Peaks"
)

plt.xlabel("Time [s]")
plt.ylabel("Amplitude [mV]")
plt.title("ECG R-Peak Detection")

plt.legend()
plt.grid()

# plt.show()
plt.savefig('C:\\git\\ecg-heart-rate-algorithm\\docs\\images\\ecg_r_peaks_detected.png')

# ============================================================
# 6. HEART RATE CALCULATION
# ============================================================

# Calculate the time intervals between consecutive R-peaks
rr_intervals = calculate_rr_intervals(
    r_peaks,
    fs
)

# Convert the RR intervals into instantaneous heart rate values
heart_rates = calculate_heart_rate(
    rr_intervals
)

print("\n--- Heart Rate Analysis ---")

print("Detected R-Peaks:")
print(len(r_peaks))

print("\nRR Intervals [s]:")
print(rr_intervals)

print("\nHeart Rates [BPM]:")
print(heart_rates)

print("\nMean RR Interval:")
print(np.mean(rr_intervals), "s")

print("\nMean Heart Rate:")
print(np.mean(heart_rates), "BPM")

# Calculate overall heart-rate statistics
mean_instantaneous_hr = np.mean(heart_rates)

hr_from_mean_rr = 60.0 / np.mean(rr_intervals)

print(
    "Mean instantaneous HR:",
    mean_instantaneous_hr,
    "BPM"
)

print(
    "HR from mean RR:",
    hr_from_mean_rr,
    "BPM"
)

rr_times = time[r_peaks[1:]]

plt.figure(figsize=(12, 4))

plt.plot(
    rr_times,
    heart_rates,
    marker="o"
)

plt.xlabel("Time [s]")
plt.ylabel("Heart Rate [BPM]")
plt.title("Instantaneous Heart Rate")

plt.grid()

#plt.show()
plt.savefig('C:\\git\\ecg-heart-rate-algorithm\\docs\\images\\heart_rate.png')


# ============================================================
# 7. REFERENCE DATA
# ============================================================

# Load expert-annotated reference beats for validation
reference_peaks = load_reference_beats(config["record"])

# Keep only reference beats located inside the analyzed signal
reference_peaks = reference_peaks[
    reference_peaks < len(ecg_segment)
]

#print("Detected peaks:")
#print(r_peaks)

#print("Reference annotations:")
#print(reference_peaks)

#for sample, symbol in zip(
#    reference_peaks,
#    reference_symbols
#):
#    if sample < len(ecg_segment):
#        print(sample, symbol)

# ============================================================
# 8. ALGORITHM VALIDATION
# ============================================================

# Compare the detected R-peaks against the reference annotations
tp, fp, fn, timing_errors, false_positive_peaks = evaluate_detection(
    r_peaks,
    reference_peaks,
    fs,
    config
)

# Calculate detection performance metrics
sensitivity, ppv = calculate_metrics(
    tp,
    fp,
    fn
)

print("\n--- Validation Results ---")

print("True Positives:", tp)
print("False Positives:", fp)
print("False Negatives:", fn)

print(
    "Sensitivity:",
    sensitivity * 100,
    "%"
)

print(
    "PPV:",
    ppv * 100,
    "%"
)

print(
    "Timing errors [samples]:",
    timing_errors
)

# ============================================================
# 9. VALIDATION RESULTS
# ============================================================

print("\n--- Full Record Validation ---")

print("Reference beats:", len(reference_peaks))
print("Detected peaks:", len(r_peaks))

print("True Positives:", tp)
print("False Positives:", fp)
print("False Negatives:", fn)

print("Sensitivity:", sensitivity * 100, "%")
print("PPV:", ppv * 100, "%")

print(
    "Mean absolute timing error [samples]:",
    np.mean(np.abs(timing_errors))
)

print(
    "Maximum timing error [samples]:",
    np.max(np.abs(timing_errors))
)

print(
    "Mean absolute timing error [ms]:",
    np.mean(np.abs(timing_errors)) / fs * 1000
)

print(
    "Maximum timing error [ms]:",
    np.max(np.abs(timing_errors)) / fs * 1000
)

# Report false-positive positions for subsequent root-cause analysis
print(
    "False Positive Peaks:",
    false_positive_peaks
)

print(
    "False Positive Times [s]:",
    false_positive_peaks / fs
)


heart_rate = test_heart_rate_for_one_second_rr_interval
print ("\nHeart Rate: ", heart_rate)


# ============================================================
# 10. FALSE POSITIVE ANALYSIS
# ============================================================

if len(false_positive_peaks) > 0:

    # Analyze the first false-positive detection
    fp_peak = false_positive_peaks[0]

    # Define a +/- 2 second analysis window
    window_seconds = 2
    window_samples = int(window_seconds * fs)

    start = max(
        0,
        fp_peak - window_samples
    )

    end = min(
        len(filtered_ecg),
        fp_peak + window_samples
    )

    # Generate time axis for the selected signal window
    local_time = np.arange(start, end) / fs

    # Select detected R-peaks located inside the analysis window
    local_detected_peaks = r_peaks[
        (r_peaks >= start)
        & (r_peaks < end)
    ]

    # Select reference beats located inside the analysis window
    local_reference_peaks = reference_peaks[
        (reference_peaks >= start)
        & (reference_peaks < end)
    ]

    # Plot the filtered ECG signal
    plt.figure(figsize=(12, 5))

    plt.plot(
        local_time,
        filtered_ecg[start:end],
        label="Filtered ECG"
    )

    # Plot all detected R-peaks in the selected window
    plt.plot(
        local_detected_peaks / fs,
        filtered_ecg[local_detected_peaks],
        "rx",
        markersize=9,
        label="Detected R-Peaks"
    )

    # Plot the reference annotations
    plt.plot(
        local_reference_peaks / fs,
        filtered_ecg[local_reference_peaks],
        "go",
        fillstyle="none",
        markersize=10,
        label="Reference Beats"
    )

    # Highlight the false-positive detection
    plt.plot(
        fp_peak / fs,
        filtered_ecg[fp_peak],
        "kx",
        markersize=14,
        markeredgewidth=3,
        label="False Positive"
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude [mV]")
    plt.title(
        "False Positive Analysis "
        f"around {fp_peak / fs:.2f} s"
    )

    plt.legend()
    plt.grid()

    plt.show()