import time
import datetime
from zatopos import EAR_NUM_MICS, EAR_WINDOW_LEN, get_ear_agent
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

READ_TIMES = 5
SOUND_LEN = READ_TIMES * EAR_WINDOW_LEN


if __name__ == "__main__":
    agent = get_ear_agent()

    time.sleep(1.0)

    fig = plt.figure()
    x = np.arange(SOUND_LEN)
    y = np.ndarray((EAR_NUM_MICS, SOUND_LEN), dtype=np.int16)

    def update_func(frame, x, y):
        plt.cla()
        plt.ylim(0,1100)

        s = datetime.datetime.now()
        for i in range(READ_TIMES):
            y[:, i * EAR_WINDOW_LEN : (i+1) * EAR_WINDOW_LEN] = agent.read_sound()
            while True:
                time.sleep(0.005)
                e = datetime.datetime.now()
                if (e-s).microseconds > 32000:
                    s = e
                    break

        for ch in range(EAR_NUM_MICS):
            plt.plot(x, y[ch])

    fanim = matplotlib.animation.FuncAnimation(
        fig=fig,
        func=update_func,
        fargs=(x,y),
        interval=300,
        frames=range(32),
        repeat=True
    )

    plt.show()
