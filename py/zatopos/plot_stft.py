import time
import scipy.fft
from worker_agent import SOUND_DEPTH, NUM_MIC_CHS, WorkerAgentSerial
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np


if __name__ == "__main__":
    agent = WorkerAgentSerial("/dev/ttyACM0")

    time.sleep(1.0)

    fig = plt.figure()
    x = np.arange(64)
    y = 512 * np.ones((SOUND_DEPTH,), dtype=np.int16)

    def update_func(frame, x, y):
        plt.cla()
        plt.ylim(0,1100)
        y = agent.read_sound()
        for ch in range(NUM_MIC_CHS):
            plt.plot(x, y[ch])

    fanim = matplotlib.animation.FuncAnimation(
        fig=fig,
        func=update_func,
        fargs=(x,y),
        interval=200,
        frames=range(32),
        repeat=True
    )

    plt.show()
    # fanim.save('sin.gif', writer='pillow')
