# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

import numpy as np

from ._ear_driver import EAR_WINDOW_LEN, EAR_WINDOW_TIME

FREQ_TO_INDEX = EAR_WINDOW_LEN * EAR_WINDOW_LEN / EAR_WINDOW_TIME

def fft_eig(sounds:np.ndarray, min_freq_index:int=None, max_freq_index:int=None):
    assert len(sounds.shape) == 3

    X = np.fft.fft(sounds).astype(np.complex64)
    # X
    #   type: np.ndarray
    #     shape: (number of samples, number of microphones, SOUND_DEPTH)
    #     dtype: np.complex64
    min_f, max_f = _correct_freq_index(min_freq_index, max_freq_index)
    X = X[:,:,min_f:max_f+1]

    R = np.einsum(
        "kif,kjf->kfij",
        X, X.conjugate()
    )
    R = np.mean(R, axis=0)

    eigval, eigvec = np.linalg.eigh(R)
    eigval = eigval[:, ::-1]    # Descending order
    eigvec = eigvec[:, ::-1, :] # Same order as eigval

    return eigval.copy(), eigvec.copy()


def _correct_freq_index(min_freq_index:int|None, max_freq_index:int|None) -> tuple[int,int]:
    min_f = 1 # default value
    max_f = int(EAR_WINDOW_LEN / 2 - 1) # default value
    if min_freq_index is not None and 1 <= min_freq_index < max_f:
        min_f = min_freq_index
    if max_freq_index is not None and 1 <= max_freq_index < max_f:
        max_f = max_freq_index
    if max_f < min_f:
        raise ValueError("Incorrect frequency index")
    return min_f, max_f


def min_freq_to_index(freq:float) -> int:
    i = np.max(
        np.ceil(FREQ_TO_INDEX * freq),
        1
    )
    i = np.min(i, np.ceil((EAR_WINDOW_LEN - 1)/2))
    return int(i)


def max_freq_to_index(freq:float) -> int:
    i = np.min(
        np.floor(FREQ_TO_INDEX * freq),
        np.ceil((EAR_WINDOW_LEN - 1)/2)
    )
    i = np.max(i, 1)
    return int(i)
