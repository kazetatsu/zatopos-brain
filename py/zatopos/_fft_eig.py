# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

import numpy as np

from ._ear_agent import EAR_WINDOW_LEN, EAR_WINDOW_TIME

def get_signal_spaces(sounds:np.ndarray, freq_filter:np.ndarray = None):
    assert len(sounds.shape) == 3

    X = np.fft.fft(sounds).astype(np.complex64)
    # X
    #   type: np.ndarray
    #     shape: (number of samples, number of microphones, SOUND_DEPTH)
    #     dtype: np.complex64
    if freq_filter is not None:
        X = X[:,:,freq_filter]
    else:
        X = X[:, :, 1:np.uint16(np.ceil(X.shape[2] / 2))]

    R = np.einsum(
        "kif,kjf->kfij",
        X, X.conjugate()
    )
    R = np.mean(R, axis=0)

    _, eigvec = np.linalg.eigh(R)
    eigvec = eigvec[:, ::-1, :] # descending order of eigen value

    return eigvec.copy()


def get_freq_filter(min_freq:float, max_freq:float):
    coef = EAR_WINDOW_LEN * EAR_WINDOW_LEN / EAR_WINDOW_TIME

    min_f = np.max(
        np.ceil(coef * min_freq),
        0
    )
    max_f = np.min(
        np.floor(coef * max_freq),
        np.ceil((EAR_WINDOW_LEN - 1)/2)
    )

    assert min_f <= max_f

    return np.arange(min_f, max_f + 1)
