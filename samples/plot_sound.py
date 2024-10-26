import time
import datetime
from zatopos import EAR_NUM_MICS, EAR_WINDOW_LEN, get_ear_driver
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

RECEIVE_TIMES = 3
SOUND_LEN = RECEIVE_TIMES * EAR_WINDOW_LEN


if __name__ == "__main__":
    driver = get_ear_driver()

    time.sleep(1.0)

    fig = plt.figure()
    x = np.arange(SOUND_LEN)
    y = np.ndarray((RECEIVE_TIMES, EAR_WINDOW_LEN, EAR_NUM_MICS), dtype=np.int16)

    def update_func(frame, x, y):
        plt.cla()
        plt.ylim(0,1100)

        driver.receive(y)

        for ch in range(EAR_NUM_MICS):
            plt.plot(x, y.reshape(SOUND_LEN, EAR_NUM_MICS)[:,ch])

    fanim = matplotlib.animation.FuncAnimation(
        fig=fig,
        func=update_func,
        fargs=(x,y),
        interval=300,
        frames=range(32),
        repeat=True
    )

    plt.show()
