import csv

import pandas as pd

import cpucluster
import ramcluster
import dscluster
import bwcluster

path  =  "/Users/gaithrjoub/Desktop/pro/ramprobx.csv"
path1 = "/Users/gaithrjoub/Desktop/pro/cpuprobx.csv"
path2 = "/Users/gaithrjoub/Desktop/pro/bwprobx.csv"
path3 = "/Users/gaithrjoub/Desktop/pro/dsprobx.csv"


CPU = pd.read_csv(path1)
CPU = pd.DataFrame(CPU)
CPU=CPU.sort_values(['index'])
print(CPU)

Memory = pd.read_csv(path)
Memory = pd.DataFrame(Memory)
Memory=Memory.sort_values(['index'])
print(Memory)

BW = pd.read_csv(path2)
BW = pd.DataFrame(BW)
BW=BW.sort_values(['index'])
print(BW)


Disk = pd.read_csv(path3)
Disk = pd.DataFrame(Disk)
Disk=Disk.sort_values(['index'])
print(Disk)


finalprob=(CPU['prob']+Memory['prob']+BW['prob']+Disk['prob'])/len('prob')*100
pd.DataFrame(finalprob)

finalprob = pd.DataFrame(finalprob)




result = pd.concat([ finalprob, CPU['CPU'], Memory['RAM'], BW['BW'], Disk['DS']], axis=1)


#finalprob['CPU']=CPU['1']
# finalprob['BW']=BW['1']
# finalprob['Disk']=Disk['1']
# finalprob['Memory']=Memory['1']



# finalprob=finalprob.sort_values(['prob'])

print(result)

result.to_csv('/Users/gaithrjoub/Desktop/pro/taskprobx.csv')