import numpy as np
import serial
import sys
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Scope(object):
    def __init__(self, ax1, ax2, maxt=10, dt=0.01):
        self.ax1 = ax1
        self.ax2 = ax2
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.y1data = [0]
        self.y2data = [0]
        self.line1 = Line2D(self.tdata, self.y1data)
        self.line2 = Line2D(self.tdata, self.y2data)
        self.line = [self.line1, self.line2]
        self.ax1.add_line(self.line1)
        self.ax1.set_ylim(-1.1, 5.1)
        self.ax1.set_xlim(0, self.maxt)
        self.ax2.add_line(self.line2)
        self.ax2.set_ylim(-1.1, 5.1)
        self.ax2.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.y1data = [self.y1data[-1]]
            self.y2data = [self.y2data[-1]]
            self.ax1.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax1.figure.canvas.draw()
            self.ax2.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax2.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.y1data.append(y[0])
        self.y2data.append(y[1])
        self.line1.set_data(self.tdata, self.y1data)
        self.line2.set_data(self.tdata, self.y2data)
        return self.line


def emitter():
    value1 = 0
    value2 = 0
    try:
        prepare = ser.readline()
        print prepare
        value1, value2 = prepare.split('|')
        value1 = int(value1)
        value2 = int(value2.replace('\r\n', ''))
    except Exception as e:
        value1 = 0
        value2 = 0
    voltage1 = float(value1)
    voltage2 = float(value2)
    voltage1 = 5*(voltage1/1024)
    voltage2 = 5*(voltage2/1024)
    voltage = [voltage1, voltage2]
    yield voltage

# Fixing random state for reproducibility
# np.random.seed(19680801)
portnmbr = str(sys.argv[1])
ser = serial.Serial('/dev/ttyACM'+portnmbr, 9600)

fig, (ax1, ax2) = plt.subplots(2, 1)
scope = Scope(ax1, ax2)

# ass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=10,
                              blit=True)


plt.show()