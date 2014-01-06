#!/usr/bin/python

import os

FREE_MEMORY = "freeMemory"
USED_MEMORY = "usedMemory"
TOTAL_MEMORY = "totalMemory"
CPU = "cpu"
CPUS = "cpus"
CPUS_DETAILS = "cpus details"
lastSysDict = {}
ALL_STRING_INDEX = 0
CPU_STRING_INDEX = 0
CPU_AND_CLOSER_STRING_INDEX = 0

def updateLastSysDict():
    cpuSysString = (os.popen("sar -P ALL 1 1").read()).split()
    updateStringIndexes(cpuSysString)
    lastSysDict[CPU] = float(cpuSysString[ALL_STRING_INDEX+1])
    lastSysDict[CPUS] = int(cpuSysString[CPU_AND_CLOSER_STRING_INDEX-1][1])
    
    cpusArray = []
    lastSysDict[CPUS_DETAILS] = cpusArray
    for i in range(lastSysDict[CPUS]):
	cpusArray.append(cpuSysString[ALL_STRING_INDEX+1 + (i+1)*(ALL_STRING_INDEX-CPU_STRING_INDEX)])

def updateStringIndexes(cpuSysString):
    global ALL_STRING_INDEX
    global CPU_STRING_INDEX
    global CPU_AND_CLOSER_STRING_INDEX
    ALL_STRING_INDEX=cpuSysString.index("all")
    CPU_AND_CLOSER_STRING_INDEX=cpuSysString.index("CPU)")
    CPU_STRING_INDEX=cpuSysString.index("CPU")
    lastSysDict[CPU] = float(cpuSysString[ALL_STRING_INDEX+1])

def updateLastSysDictMemory():
    memorySysString = (os.popen("free -m").read()).split()
    lastSysDict[FREE_MEMORY] = float(memorySysString[16])
    lastSysDict[USED_MEMORY] = float(memorySysString[15])
    lastSysDict[TOTAL_MEMORY] = float(memorySysString[7])
