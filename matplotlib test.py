import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.animation import FuncAnimation


def update_plot(num, data, sc):
    print(data[num])
    print()
    sc._offsets3d = data[num]
    sc.set_color(["red"])
    if False:
        ani.event_source.stop()
    return sc


numframes = 10
data = np.random.rand(numframes, 3, 1)  # a (time, position) array

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ix, iy, iz = data[0]
sc = ax.scatter(ix, iy, iz, c="k")
ani = FuncAnimation(fig, update_plot, frames=numframes, interval=500, fargs=(data, sc))
plt.show()
