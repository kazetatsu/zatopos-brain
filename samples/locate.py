import matplotlib.pyplot as plt
import numpy as np
import datetime

import zatopos

if __name__ == "__main__":
    x = []
    x.append(np.loadtxt("data/sound000.csv", dtype=np.float32))
    x.append(np.loadtxt("data/sound001.csv", dtype=np.float32))
    x.append(np.loadtxt("data/sound002.csv", dtype=np.float32))
    x = np.array(x)

    eigval, eigvec = zatopos.fft_eig(x, min_freq_index=16, max_freq_index=25)
    print(eigvec)

    result = np.zeros((10,8,8),dtype=np.float32)

    music = zatopos.Musical(min_freq_index=16, max_freq_index=25)

    s = datetime.datetime.now()
    music.search(eigvec, result)
    e = datetime.datetime.now()
    print(e-s)

    sn_ratio = eigval[:,0] / eigval.sum(axis=1)
    sn_max_if = np.argmax(sn_ratio) # Frequency index which has max S/N(signal noise) ratio
    print("S/N max")
    print(sn_max_if)
    print("result as text")
    print(result[sn_max_if])

    plt.figure()
    plt.imshow(result[sn_max_if])
    plt.show()
