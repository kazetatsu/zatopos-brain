import numpy as np

from .worker_agent import WorkerAgentBase, CH_NUM, SOUND_DEPTH

def locate(worker_agent:WorkerAgentBase, sampling_time:float, mic_pos:np.ndarray):
    x_ = worker_agent.read_sound()
    X = np.ndarray((CH_NUM, SOUND_DEPTH), dtype=np.complex64)
    for ch in range(CH_NUM):
        X[ch] = np.fft.fft(x_[ch]).astype(np.complex64)
    R = np.einsum(
        "if,jf->fij",
        X, X.conjugate()
    )

    f = np.fft.fftfreq(n=SOUND_DEPTH, d=sampling_time)

    eigval, eigvec = np.linalg.eigh(R)
    eigval = eigval[:, ::-1] # descending order
    eigvec = eigvec[:, ::-1, :] # same order as eigval

    E = eigvec[:,1:,:]
    c = np.float32(340)
    d = np.float32(0.06)
    tau = (1j * d / c) * np.exp(2.0 * np.pi * np.arange(CH_NUM))


