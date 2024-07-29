import time
from worker_agent import CH_NUM, WorkerAgentSerial
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

SOUND_LENGTH = 256

if __name__ == "__main__":
    agent = WorkerAgentSerial("/dev/ttyACM0")

    time.sleep(1.0)

    fig = plt.figure()
    x = np.arange(SOUND_LENGTH)
    y = np.ndarray((CH_NUM, SOUND_LENGTH), dtype=np.int16)

    def update_func(frame, x):
        plt.cla()
        plt.ylim(0,1100)
        y = agent.read_sound(SOUND_LENGTH)
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
