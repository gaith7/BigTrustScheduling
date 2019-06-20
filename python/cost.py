import csv

import pandas as pd
import random


path = "/Users/gaithrjoub/Desktop/gaith1.csv"

# colnames = list('ABCDEFGHIKLMNO')
datagaith = pd.read_csv(path)
datagaith = pd.DataFrame(datagaith)

Q = list((map(float,datagaith['Memory usage [KB]'])))

K = list((map(float,datagaith['Timestamp [ms]'])))

R = list((map(float,datagaith['CPU usage [MHZ]'])))

B = list((map(float,datagaith['Network transmitted throughput [KB/s]'])))

D = list((map(float,datagaith['	Disk write throughput [KB/s]'])))

my_randoms=[]

for i in range (len(K)):

    my_randoms.append(random.randrange(180000000,1098798788))

K=my_randoms
# R = list((map(float,datagaith['Network transmitted throughput [KB/s]'])))


# J=datagaith['Network transmitted throughput [KB/s]']

# print(Q)
# length=len(j)
J=pd.DataFrame(list(zip(K,Q,R,B,D)))


print(J)

# print(Q)
# length=len(j)


# print(J)


costRAM1=[]
costRAM2=[]
costRAM3=[]
costRAM4=[]
costRAM5=[]
costCPU1=[]
costCPU2=[]
costCPU3=[]
costCPU4=[]
costCPU5=[]
costBW1=[]
costBW2=[]
costBW3=[]
costBW4=[]
costBW5=[]
costDS1=[]
costDS2=[]
costDS3=[]
costDS4=[]
costDS5=[]


for index,i in J.iterrows():

    if i[1] <= 128000 :
       costRAM1.append(0.05*i[0]/3600000)
    elif i [1] <= 256000  and i [1] > 128000 :
       costRAM2.append(0.1*i[0]/3600000)
    elif i[1] <= 512000  and i[1] > 256000 :
        costRAM3.append(0.2*i[0]/3600000)
    elif i[1] <= 1024000  and i[1] > 512000 :
        costRAM4.append(0.3*i[0]/3600000)
    #if J [1] > 1048576 and  J [2] > 1400 :
    else:
        costRAM5.append(0.4*i[0]/3600000)

    if i[2] <= 600:
        costCPU1.append (i[0]/3600000 * 0.05)
    elif i[2] <= 1200 and i[2] > 600:
        costCPU2.append (i[0]/3600000 * 0.1)
    elif  i[2] <= 2000 and i[2] > 1200:
        costCPU3.append (i[0]/3600000 * 0.2)
    elif  i[2] <= 2400 and i[2] > 2000:
        costCPU4.append (i[0]/3600000 * 0.3)
    # if J [1] > 1048576 and  J [2] > 1400 :
    else:
        costCPU5.append (i[0]/3600000 * 0.4)

    if i[3] <= 1:
            costBW1.append (0.05 * i[0]/3600000)
    elif i[3] <= 2.5 and i[3] > 1:
            costBW2.append (0.1*i[0]/3600000)
    elif i[3] <= 10 and i[3] > 2.5:
            costBW3.append (0.2*i[0]/3600000)
    elif i[3] <= 15 and i[3] > 10:
            costBW4.append (0.3*i[0]/3600000)
        # if J [1] > 1048576 and  J [2] > 1400 :
    else:
            costBW5.append (0.4*i[0]/3600000)

    if i[4] <= 1:
        costDS1.append ((0.198 * (i[4]*10)) * (i[0] /3600000))
    elif i[4] <= 1.3 and i[4] > 1:
        costDS2.append ((0.198 * (i[4]*10)) * (i[0] /3600000))
    elif i[4] <= 1.6 and i[4] > 1.3:
        costDS3.append ((0.198 * (i[4]*10))* (i[0] /3600000))
    elif i[3] <= 2 and i[3] > 1.6:
        costDS4.append ((0.198 * (i[4]*10))* (i[0] /3600000))
        # if J [1] > 1048576 and  J [2] > 1400 :
    else:
        costDS5.append ((0.198 * (i[4]*10)) * (i[0] /3600000))

print(len('costRAM1'))
print(costRAM1)
print('costRAM2')
print(costRAM2)
print('costRAM3')
print(costRAM3)
print('costRAM4')
print(costRAM4)
print(len('costRAM5'))
print(costRAM5)


print(len('costCPU1'))
print(costCPU1)
print('costCPU2')
print(costCPU2)
print('costCPU3')
print(costCPU3)
print('costCPU4')
print(costCPU4)
print(len('costCPU5'))
print(costCPU5)

print(len('costBW1'))
print(costBW1)
print('costBW2')
print(costBW2)
print('costBW3')
print(costBW3)
print('costBW4')
print(costBW4)
print('costBW5')
print(costBW5)


print(len('costDS1'))
print(costDS1)
print('costDS2')
print(costDS2)
print('costDS3')
print(costDS3)
print('costDS4')
print(costDS4)
print('costDS5')
print(costDS5)

print(J)

J.to_csv("/Users/gaithrjoub/Desktop/FINALCOST.csv")