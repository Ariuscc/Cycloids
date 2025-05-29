from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

class Figure:
    def __init__(self, ratio=3.25, frames=800, ncycles=1):
        self.frames = frames
        self.ncycles = ncycles
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        theta = np.linspace(0, 2 * np.pi, 150)

        self.small_r = 1.0 / ratio

        r = self.small_r
        x = r * np.cos(theta) + (1 - r)
        y = r * np.sin(theta)
        self.inner_circle, = self.ax.plot(x, y, 'k-')

        x = r * np.cos(theta) + (1 + r)
        y = r * np.sin(theta) + 0
        self.outer_circle, = self.ax.plot(x, y, 'k-')

        theta2 = np.linspace(0, 2 * np.pi, 100)
        x2 = np.cos(theta2)
        y2 = np.sin(theta2)
        self.big_circle, = self.ax.plot(x2, y2, 'b-')

        self.line1, = self.ax.plot([], [], 'k-')
        self.dot1,  = self.ax.plot([], [], 'ko', ms=5)
        self.line2, = self.ax.plot([], [], 'k-')
        self.dot2,  = self.ax.plot([], [], 'ko', ms=5)

        self.hypocycloid, = self.ax.plot([], [], 'g-')
        self.epicycloid,  = self.ax.plot([], [], 'r-')

        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)

        self.animation = FuncAnimation(
            self.fig, self.animate,
            frames=self.frames * self.ncycles,
            interval=50, blit=False,
            repeat_delay=2000,
        )

    def update_inner_circle(self, phi):
        theta = np.linspace(0, 2 * np.pi, 100)
        r = self.small_r
        x = r * np.cos(theta) + (1 - r) * np.cos(phi)
        y = r * np.sin(theta) + (1 - r) * np.sin(phi)
        self.inner_circle.set_data(x, y)

    def update_hypocycloid(self, phis):
        r = self.small_r
        x = (1 - r) * np.cos(phis) + r * np.cos((1 - r) / r * phis)
        y = (1 - r) * np.sin(phis) - r * np.sin((1 - r) / r * phis)
        self.hypocycloid.set_data(x, y)

        cx = (1 - r) * np.cos(phis[-1])
        cy = (1 - r) * np.sin(phis[-1])
        self.line1.set_data([cx, x[-1]], [cy, y[-1]])
        self.dot1.set_data([cx], [cy])

    def update_outer_circle(self, phi):
        theta = np.linspace(0, 2 * np.pi, 100)
        r = self.small_r
        x = r * np.cos(theta) + (1 + r) * np.cos(phi)
        y = r * np.sin(theta) + (1 + r) * np.sin(phi)
        self.outer_circle.set_data(x, y)

    def update_epicycloid(self, phis):
        r = self.small_r
        x = (1 + r) * np.cos(phis) - r * np.cos((1 + r) / r * phis)
        y = (1 + r) * np.sin(phis) - r * np.sin((1 + r) / r * phis)
        self.epicycloid.set_data(x, y)

        cx = (1 + r) * np.cos(phis[-1])
        cy = (1 + r) * np.sin(phis[-1])
        self.line2.set_data([cx, x[-1]], [cy, y[-1]])
        self.dot2.set_data([cx], [cy])

    def animate(self, frame):
        phi = 2 * np.pi * (frame + 1) / self.frames
        phis = np.linspace(0, phi, frame + 1)

        self.update_inner_circle(phi)
        self.update_hypocycloid(phis)
        self.update_outer_circle(phi)
        self.update_epicycloid(phis)

        return (
            self.inner_circle, self.hypocycloid,
            self.outer_circle, self.epicycloid,
            self.line1, self.dot1,
            self.line2, self.dot2,
        )

if __name__ == "__main__":
    cycl = Figure(ratio=3.4, frames=80, ncycles=5)
    writer = PillowWriter(fps=20)
    cycl.animation.save("hypo_epi.gif", writer=writer)
    plt.show()
