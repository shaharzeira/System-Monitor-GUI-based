#!/usr/bin/python

'''
Copyright (C) 2014 by Shahar Zeira (shahar.zeira@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from SysViewModel import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import math
import threading
import gobject

majorFormatter = FormatStrFormatter('%d')
minorLocatorY   = MultipleLocator(10)

xRange = range(LEN_Y_CHART)
GuiCpuDataArray = [0] * LEN_Y_CHART
GuiMemoryDataArray = [0] * LEN_Y_CHART
lockTime=0.9
detailsCpusLines = []
lock = threading.Lock()

def setLine(place, name):
    ax = plt.subplot(place)
    ax.set_xlim((0, LEN_Y_CHART - 1))
    ax.set_ylim((0, 100))
    ax.set_xlabel(name)
    ax.set_xticks([])
    ax.yaxis.set_minor_locator(minorLocatorY)
    ax.yaxis.set_minor_formatter(majorFormatter)
    return ax

def updateGuiCpuDataArray():
    global GuiCpuDataArray
    GuiCpuDataArray[-(len(cpuDataArray)):] = cpuDataArray
    for i in range(lastSysDict[CPUS]):
	GuiCpusDetailsDataArray[i][-(len(cpusDataArray[i])):] = cpusDataArray[i]

def updateGuiMemoryDataArray():
    global GuiMemoryDataArray
    GuiMemoryDataArray[-(len(memoryDataArray)):] = memoryDataArray

def adjust(a):
    return [(6.0/7*x+math.sqrt(max(x,0))*10.0/7) for x in a]
    #return a[0:]

def lockFunc(key):
    with lock:
	if key == "updateLineData":
	    global lastSysDictList
	    lastSysDictList = lastSysDictList[-3:]
	    thread.start_new_thread(updateLastSysDictList, ())

	    updateGuiMemoryDataArray()
	    updateLastSysDictMemory()
	    updateRecentMemoryDataArray()

	    updateGuiCpuDataArray()
	    updateLastSysDict()
	    updateRecentCpuDataArray()
	if key == "animate":
	    line.set_data(xRange, adjust(GuiCpuDataArray))
	    for j in range(lastSysDict[CPUS]):
		detailsCpusLines[j].set_data(xRange, adjust(GuiCpusDetailsDataArray[j]))
	if key == "animateMemory":
	    lineMemory.set_data(xRange, adjust(GuiMemoryDataArray))

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    for i in range(lastSysDict[CPUS]):
	detailsCpusLines[i].set_data([], [])
    return detailsCpusLinesTup

# animation function.  This is called sequentially
def animate(i):
    lockFunc("animate")
    return detailsCpusLinesTup

# initialization function: plot the background of each frame
def initMemory():
    lineMemory.set_data([], [])
    return lineMemory,

# animation function.  This is called sequentially
def animateMemory(i):
    lockFunc("animateMemory")
    return lineMemory,

def updateLineData():
    lockFunc("updateLineData")
    time.sleep(myInterval/1000/2)
    return True

updateLastSysDictList()
time.sleep(0.8)
while updateLastSysDict() == False:
    time.sleep(0.1)
updateRecentCpuDataArray()
GuiCpusDetailsDataArray = [[]] * lastSysDict[CPUS]

for i in range(lastSysDict[CPUS]):
    GuiCpusDetailsDataArray[i] = [0] * LEN_Y_CHART
updateLastSysDictMemory()
updateRecentMemoryDataArray()

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
fig.canvas.set_window_title('System Monitor') 

ax = setLine(211, "Cpu %")
line, = ax.plot([], [], lw=5)

for i in range(lastSysDict[CPUS]):
    ln, = ax.plot([], [], lw=1)
    detailsCpusLines.append(ln)
detailsCpusLines.append(line)
detailsCpusLinesTup=tuple(detailsCpusLines)

axMemory = setLine(212, "Memory % of total [" + str(lastSysDict[TOTAL_MEMORY]) + "]")
lineMemory, = axMemory.plot([], [], lw=2)

# call the animator.  blit=True means only re-draw the parts that have changed.
# Animate Memory usage
animMemory = animation.FuncAnimation(fig, animateMemory, init_func=initMemory,
                               frames=40, interval=myInterval, blit=True)

# Animate Cpu usage
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=40, interval=myInterval, blit=True)

gobject.idle_add(updateLineData)
plt.show()
