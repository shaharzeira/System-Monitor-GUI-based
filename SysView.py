#!/usr/bin/python

from SysViewModel import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time

xRange = range(LEN_Y_CHART)
GuiCpuDataArray = [0] * LEN_Y_CHART
GuiMemoryDataArray = [0] * LEN_Y_CHART

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
fig.canvas.set_window_title('System Monitor') 
ax = plt.subplot(211)
ax.set_xlim((0, LEN_Y_CHART - 1))
ax.set_ylim((0, 100))
ax.set_xlabel("Cpu %")
line, = ax.plot([], [], lw=5)
detailsCpusLines = []

updateLastSysDict()
updateRecentCpuDataArray()
GuiCpusDetailsDataArray = [[]] * lastSysDict[CPUS]
for i in range(lastSysDict[CPUS]):
    GuiCpusDetailsDataArray[i] = [0] * LEN_Y_CHART

for i in range(lastSysDict[CPUS]):
    ln, = ax.plot([], [], lw=1)
    detailsCpusLines.append(ln)
detailsCpusLines.append(line)
detailsCpusLinesTup=tuple(detailsCpusLines)

def updateGuiCpuDataArray():
    global GuiCpuDataArray
    GuiCpuDataArray[-(len(cpuDataArray)):] = cpuDataArray
    for i in range(lastSysDict[CPUS]):
	GuiCpusDetailsDataArray[i][-(len(cpusDataArray[i])):] = cpusDataArray[i]

def updateGuiMemoryDataArray():
    global GuiMemoryDataArray
    GuiMemoryDataArray[-(len(memoryDataArray)):] = memoryDataArray

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    for i in range(lastSysDict[CPUS]):
	detailsCpusLines[i].set_data([], [])
    return detailsCpusLinesTup

# animation function.  This is called sequentially
def animate(i):
    updateGuiCpuDataArray()
    line.set_data(xRange, GuiCpuDataArray)
    for j in range(lastSysDict[CPUS]):
	detailsCpusLines[j].set_data(xRange, GuiCpusDetailsDataArray[j])
    updateLastSysDict()
    updateRecentCpuDataArray()
    return detailsCpusLinesTup


# First set up the figure, the axis, and the plot element we want to animate
ax2 = plt.subplot(212)
ax2.set_xlim((0, LEN_Y_CHART - 1))
ax2.set_ylim((0, 100))
updateLastSysDictMemory()
updateRecentMemoryDataArray()
ax2.set_xlabel("Memory % of total [" + str(lastSysDict[TOTAL_MEMORY]) + "]")
line2, = ax2.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init2():
    time.sleep(1)
    line2.set_data([], [])
    return line2,

# animation function.  This is called sequentially
def animate2(i):
    #time.sleep(0.1)
    updateGuiMemoryDataArray()
    line2.set_data(xRange, GuiMemoryDataArray)
    updateLastSysDictMemory()
    updateRecentMemoryDataArray()
    return line2,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim2 = animation.FuncAnimation(fig, animate2, init_func=init2,
                               frames=107, interval=1070, blit=True)

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=107, interval=1070, blit=True)

plt.show()
