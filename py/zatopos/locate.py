import numpy as np

from .ear_agent import EarAgent, NUM_MIC_CHS, SOUND_DEPTH

def locate(worker_agent:EarAgent, sampling_time:float, mic_pos:np.ndarray):
    x = worker_agent.read_sound(dtype=np.float32)
    # type: np.ndarray
    #   shape: (NUM_MIC_CHS, SOUND_DEPTH)
    #   dtype: np.complex64
    X = np.fft.fft(x)
    R = np.einsum(
        "if,jf->fij",
        X, X.conjugate()
    )

    f = np.fft.fftfreq(n=SOUND_DEPTH, d=sampling_time)

    eigval, eigvec = np.linalg.eigh(R)
    eigval = eigval[:, ::-1] # descending order
    eigvec = eigvec[:, ::-1, :] # same order as eigval
