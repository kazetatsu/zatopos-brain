import time
from worker_agent import SOUND_DEPTH, CH_NUM, WorkerAgentSerial
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

SOUND_M = 5

if __name__ == "__main__":
    agent = WorkerAgentSerial("/dev/ttyACM0")

    time.sleep(1.0)

    fig = plt.figure()
    x = np.arange(SOUND_M * SOUND_DEPTH)
    y = np.ndarray((CH_NUM, SOUND_M * SOUND_DEPTH), dtype=np.int16)

    def update_func(frame, x):
        plt.cla()
        plt.ylim(0,1100)
        for i in range(SOUND_M):
            y[:, i*SOUND_DEPTH:(i+1)*SOUND_DEPTH] = agent.read_sound()
        for ch in range(CH_NUM):
            plt.plot(x, y[ch])

    fanim = matplotlib.animation.FuncAnimation(
        fig=fig,
        func=update_func,
        fargs=(x,),
        interval=300,
        frames=range(32),
        repeat=True
    )

    plt.show()
    # fanim.save('sin.gif', writer='pillow')
