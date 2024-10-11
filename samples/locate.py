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

    freq_i = np.arange(16,24, dtype=np.uint8)

    sss = zatopos.get_signal_spaces(x, freq_filter=freq_i)
    print(sss)

    locator = zatopos.Locator(freq_filter=freq_i)

    s = datetime.datetime.now()
    res = locator.locate(sss)
    e = datetime.datetime.now()
    print(e-s)

    print(res)

    plt.figure()
    plt.imshow(res)
    plt.show()
