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
import time

xRange = range(LEN_Y_CHART)
GuiCpuDataArray = [0] * LEN_Y_CHART
GuiMemoryDataArray = [0] * LEN_Y_CHART
isLock=False
lockTime=0.9

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
fig.canvas.set_window_title('System Monitor') 
ax = plt.subplot(211)
ax.set_xlim((0, LEN_Y_CHART - 1))
ax.set_ylim((0, 100))
ax.set_xlabel("Cpu %")
line, = ax.plot([], [], lw=5)
detailsCpusLines = []

thread.start_new_thread(updateSysDictListMainThread, ())
time.sleep(1.3)
while updateLastSysDict() == False:
    time.sleep(0.1)

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
    if not isLock:
	a = GuiCpuDataArray[0:]
	line.set_data(xRange, a)
	for j in range(lastSysDict[CPUS]):
	    b =GuiCpusDetailsDataArray[j][0:]
	    detailsCpusLines[j].set_data(xRange, b)
    return detailsCpusLinesTup


# First set up the figure, the axis, and the plot element we want to animate
axMemory = plt.subplot(212)
axMemory.set_xlim((0, LEN_Y_CHART - 1))
axMemory.set_ylim((0, 100))
updateLastSysDictMemory()
updateRecentMemoryDataArray()
axMemory.set_xlabel("Memory % of total [" + str(lastSysDict[TOTAL_MEMORY]) + "]")
lineMemory, = axMemory.plot([], [], lw=2)

# initialization function: plot the background of each frame
def initMemory():
    lineMemory.set_data([], [])
    return lineMemory,

# animation function.  This is called sequentially
def animateMemory(i):
    if not isLock:
	a = GuiMemoryDataArray[0:]
	lineMemory.set_data(xRange, a)
    return lineMemory,

def updateLineData():
    while True:
	isLock=True
	updateGuiMemoryDataArray()
	updateLastSysDictMemory()
	updateRecentMemoryDataArray()

	updateGuiCpuDataArray()
	updateLastSysDict()
	updateRecentCpuDataArray()
	time.sleep(myInterval/980*(1-lockTime))
	isLock=False
	time.sleep(myInterval/980*lockTime)

# call the animator.  blit=True means only re-draw the parts that have changed.
# Animate Memory usage
animMemory = animation.FuncAnimation(fig, animateMemory, init_func=initMemory,
                               frames=40, interval=myInterval, blit=True)

# Animate Cpu usage
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=40, interval=myInterval, blit=True)

thread.start_new_thread(updateLineData, ())

plt.show()
