import numpy as np

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
        X = X[:, :, 1:np.ceil((X.shape[2] - 1) / 2)]

    R = np.einsum(
        "kif,kjf->kfij",
        X, X.conjugate()
    )
    R = np.mean(R, axis=0)

    _, eigvec = np.linalg.eigh(R)
    eigvec = eigvec[:, ::-1, :] # descending order of eigen value

    return eigvec.copy()


def get_freq_filter(min_freq:float, max_freq:float, sampling_time:float = None, sampling_depth:int = None):
    assert sampling_time > 0
    assert sampling_depth > 0

    if sampling_time is not None:
        l = sampling_time
    else:
        l = SOUND_SAMPLING_TIME

    if sampling_depth is not None:
        n = sampling_depth
    else:
        n = SOUND_DEPTH

    min_f = np.max(
        np.ceil(n * n * min_freq / l),
        0
    )
    max_f = np.min(
        np.floor(n * n * max_freq / l),
        np.ceil((n - 1)/2)
    )

    assert min_f <= max_f

    return np.arange(min_f, max_f + 1)
