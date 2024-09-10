import time
import datetime
from zatopos import NUM_MIC_CHS, SOUND_DEPTH, get_ear_agent
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

READ_TIMES = 5
SOUND_LEN = READ_TIMES * SOUND_DEPTH


if __name__ == "__main__":
    agent = get_ear_agent()

    time.sleep(1.0)

    fig = plt.figure()
    x = np.arange(SOUND_LEN)
    y = np.ndarray((NUM_MIC_CHS, SOUND_LEN), dtype=np.int16)

    def update_func(frame, x, y):
        plt.cla()
        plt.ylim(0,1100)

        s = datetime.datetime.now()
        for i in range(READ_TIMES):
            y[:, i * SOUND_DEPTH : (i+1) * SOUND_DEPTH] = agent.read_sound()
            while True:
                time.sleep(0.005)
                e = datetime.datetime.now()
                if (e-s).microseconds > 32000:
                    s = e
                    break

        for ch in range(NUM_MIC_CHS):
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
