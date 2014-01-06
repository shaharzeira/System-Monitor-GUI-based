#!/usr/bin/python

from memorySysModel import *

LEN_Y_CHART = 61
cpuDataArray = []
memoryDataArray = []
cpusDataArray = []

def updateRecentCpuDataArray():
    updateCpuDataArray(lastSysDict)

def updateCpuDataArray(d):
    cpuDataArray.append(d.get(CPU))
    if len(cpuDataArray) > LEN_Y_CHART:
	cpuDataArray.pop(0)
    for i in range(lastSysDict[CPUS]):
	if len(cpusDataArray) < lastSysDict[CPUS]:
	    cpusDataArray.append([])
	cpusDataArray[i].append(d.get(CPUS_DETAILS)[i])
	if len(cpusDataArray[i]) > LEN_Y_CHART:
	    cpusDataArray[i].pop(0)

def updateRecentMemoryDataArray():
    updateMemoryDataArray(lastSysDict)

def updateMemoryDataArray(d):
    memoryDataArray.append(d.get(USED_MEMORY) / d.get(TOTAL_MEMORY) * 100)
    if len(memoryDataArray) > LEN_Y_CHART:
	memoryDataArray.pop(0)
