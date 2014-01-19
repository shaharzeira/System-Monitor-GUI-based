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

import os
import thread
import time

FREE_MEMORY = "freeMemory"
USED_MEMORY = "usedMemory"
TOTAL_MEMORY = "totalMemory"
CPU = "cpu"
CPUS = "cpus"
CPUS_DETAILS = "cpus details"
lastSysDict = {}
lastSysDictList = []
ALL_STRING_INDEX = 0
CPU_STRING_INDEX = 0
CPU_AND_CLOSER_STRING_INDEX = 0
myInterval =840.0

def updateLastSysDict():
    if len(lastSysDictList) > 0:
	cpuSysString = lastSysDictList[-1]
	updateStringIndexes(cpuSysString)
	lastSysDict[CPU] = float(cpuSysString[ALL_STRING_INDEX+1])
	lastSysDict[CPUS] = int(cpuSysString[CPU_AND_CLOSER_STRING_INDEX-1][1])
    
	cpusArray = []
	lastSysDict[CPUS_DETAILS] = cpusArray
	for i in range(lastSysDict[CPUS]):
	    cpusArray.append(cpuSysString[ALL_STRING_INDEX+1 + (i+1)*(ALL_STRING_INDEX-CPU_STRING_INDEX)])
	return True
    else:
	return False

def updateStringIndexes(cpuSysString):
    global ALL_STRING_INDEX
    global CPU_STRING_INDEX
    global CPU_AND_CLOSER_STRING_INDEX
    ALL_STRING_INDEX=cpuSysString.index("all")
    CPU_AND_CLOSER_STRING_INDEX=cpuSysString.index("CPU)")
    CPU_STRING_INDEX=cpuSysString.index("CPU")

def updateLastSysDictMemory():
    memorySysString = (os.popen("free -m").read()).split()
    lastSysDict[FREE_MEMORY] = float(memorySysString[16])
    lastSysDict[USED_MEMORY] = float(memorySysString[15])
    lastSysDict[TOTAL_MEMORY] = float(memorySysString[7])

def updateLastSysDictList():
    t =(os.popen("sar -P ALL 1 1").read()).split()
    lastSysDictList.append(t)

def updateSysDictListMainThread():
    while True:
	global lastSysDictList
	lastSysDictList = lastSysDictList[-3:]
	thread.start_new_thread(updateLastSysDictList, ())
	time.sleep(myInterval/930)
