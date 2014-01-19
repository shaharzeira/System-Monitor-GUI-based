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

from SysModel import *

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
	cpusDataArray[i].append(float(d.get(CPUS_DETAILS)[i]))
	if len(cpusDataArray[i]) > LEN_Y_CHART:
	    cpusDataArray[i].pop(0)

def updateRecentMemoryDataArray():
    updateMemoryDataArray(lastSysDict)

def updateMemoryDataArray(d):
    memoryDataArray.append(d.get(USED_MEMORY) / d.get(TOTAL_MEMORY) * 100)
    if len(memoryDataArray) > LEN_Y_CHART:
	memoryDataArray.pop(0)
