import numpy as np


def remove_mean(ecg):
    return ecg - np.mean(ecg)