import csv
import math
import numpy as np
import pandas as pd
from numpy import percentile
from scipy.stats import iqr

import functools
import matplotlib.pyplot as plt
import seaborn; seaborn.set()  # set plot style
from sklearn.cluster import KMeans

path = "/Users/gaithrjoub/Desktop/pro/1_exported.csv"

datagaith = pd.read_csv(path)
datagaith = pd.DataFrame(datagaith)
R = list((map(float,datagaith['	Network transmitted throughput [KB/s]'])))
# print(R)


path1 = "/Users/gaithrjoub/Desktop/pro/generated_time.csv"
Q = pd.read_csv(path1)
Q = pd.DataFrame(Q)
Q = list((map(int,Q['# time'])))

#
J=pd.DataFrame(list(zip(Q,R)))

data = J[1]
df = data.sort_values()

q25, q75 = percentile(df, 25), percentile(df, 75)
iqr = q75 - q25

# calculate the outlier cutoff
cut_off = iqr * 1.5
lower, upper = q25 - cut_off, q75 + cut_off



print (lower)
print (upper)

lowerlist_CPU=[]
uperlist_CPU=[]
medianlist_CPU=[]
list=[]
for index, i in df.iteritems():
    if i >= upper:
        uperlist_CPU.append(index)
    elif i <= lower :
        lowerlist_CPU.append(index)
    else:
        medianlist_CPU.append(index)

print('//////////////////')

print((lowerlist_CPU))
print((medianlist_CPU))
print((uperlist_CPU))

cost=[]

for index, i in J.iterrows ():
        # and i [2] <= 200
    if i[1] <= 1:
            cost.append (i[0] / 3600000 * 0.05)
    elif i[1] <= 2.5 and i[1] > 1:
            cost.append (i[0] / 3600000 * 0.1)
    elif i[1] <= 10 and i[1] > 2.5:
            cost.append (i[0] / 3600000 * 0.2)
    elif i[1] <= 15 and i[1] > 10:
            cost.append (i[0] / 3600000 * 0.3)
            # if J [1] > 1048576 and  J [2] > 1400 :
    else:

            cost.append (i[0] / 3600000 * 0.4)

print (pd.np.std (cost))


X = pd.np.asarray (cost)

X = X.reshape (-1, 1)

true_k = 5
model = KMeans (n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit (X)

labels = model.predict (X)

labels = pd.DataFrame (labels)

print (labels)

documents=pd.DataFrame((cost))
documents["label"]=labels



print(documents["label"])


documents.to_csv('/Users/gaithrjoub/Desktop/pro/bw_cluster.csv')


cost1=[]
cost2=[]
cost3=[]
cost4=[]
cost5=[]

for index,i in documents.iterrows():
    # and i [2] <= 200
    if i['label'] == 0:
       cost1.append(index)
    #    and i[2] <= 400 and i[2] > 200
    elif i['label'] == 1:
       cost2.append(index)
    #     and i[2] <= 800 and i[2] > 400
    elif i['label'] == 2:
        cost3.append(index)
    #      and i[2] <= 1400 and i[2] > 800
    elif  i['label'] == 3:
        cost4.append(index)
    #if J [1] > 1048576 and  J [2] > 1400 :
    else:
        cost5.append(index)



lowcase1=[]
medcase1=[]
upcase1=[]

print('cost1')
print((cost1))
print('cost2')
print((cost2))
print('cost3')
print((cost3))
print('cost4')
print((cost4))
print('cost5')
print((cost5))
print('****')


lowcase1=[]
medcase1=[]
upcase1=[]

for i in cost1:
    if i in lowerlist_CPU:
        lowcase1.append(i)
    elif i in medianlist_CPU:
        medcase1.append(i)
    elif i in uperlist_CPU:
        upcase1.append(i)

upcase1=pd.DataFrame(upcase1)
upcase1['prob']=3/15

medcase1=pd.DataFrame(medcase1)
medcase1['prob']=2/15

lowcase1=pd.DataFrame(lowcase1)
lowcase1['prob']=1/15

framescase1 = upcase1.append(medcase1, ignore_index=True)
framescase1 = framescase1.append(lowcase1, ignore_index=True)


lowcase2=[]
medcase2=[]
upcase2=[]

for i in cost2:
    if i in lowerlist_CPU:
        lowcase2.append(i)
    elif i in medianlist_CPU:
        medcase2.append(i)
    elif i in uperlist_CPU:
        upcase2.append(i)

upcase2=pd.DataFrame(upcase2)
upcase2['prob']=6/15

medcase2=pd.DataFrame(medcase2)
medcase2['prob']=4/15

lowcase2=pd.DataFrame(lowcase2)
lowcase2['prob']=2/15

framescase2 = upcase2.append(medcase2, ignore_index=True)
framescase2 = framescase2.append(lowcase2, ignore_index=True)


lowcase3=[]
medcase3=[]
upcase3=[]

for i in cost3:
    if i in lowerlist_CPU:
        lowcase3.append(i)
    elif i in medianlist_CPU:
        medcase3.append(i)
    elif i in uperlist_CPU:
        upcase3.append(i)

upcase3=pd.DataFrame(upcase3)
upcase3['prob']=9/15

medcase3=pd.DataFrame(medcase3)
medcase3['prob']=6/15

lowcase3=pd.DataFrame(lowcase3)
lowcase3['prob']=3/15

framescase3 = upcase3.append(medcase3, ignore_index=True)
framescase3 = framescase3.append(lowcase3, ignore_index=True)


lowcase4=[]
medcase4=[]
upcase4=[]

for i in cost4:
    if i in lowerlist_CPU:
        lowcase4.append(i)
    elif i in medianlist_CPU:
        medcase4.append(i)
    elif i in uperlist_CPU:
        upcase4.append(i)

upcase4=pd.DataFrame(upcase4)
upcase4['prob']=12/15

medcase4=pd.DataFrame(medcase4)
medcase4['prob']=8/15

lowcase4=pd.DataFrame(lowcase4)
lowcase4['prob']=4/15

framescase4 = upcase4.append(medcase4, ignore_index=True)
framescase4 = framescase4.append(lowcase4, ignore_index=True)



lowcase5=[]
medcase5=[]
upcase5=[]

for i in cost5:
    if i in lowerlist_CPU:
        lowcase5.append(i)
    elif i in medianlist_CPU:
        medcase5.append(i)
    elif i in uperlist_CPU:
        upcase5.append(i)

upcase5=pd.DataFrame(upcase5)
upcase5['prob']=15/15

medcase5=pd.DataFrame(medcase5)
medcase5['prob']=10/15

lowcase5=pd.DataFrame(lowcase5)
lowcase5['prob']=5/15

framescase5 = upcase5.append(medcase5, ignore_index=True)
framescase5 = framescase5.append(lowcase5, ignore_index=True)

frames = framescase5.append(framescase4, ignore_index=True)
frames = frames.append(framescase3, ignore_index=True)
frames = frames.append(framescase2, ignore_index=True)
frames = frames.append(framescase1, ignore_index=True)



# frames['index']=frames[0]
print('****************')
# result = pd.concat(frames)
#frames=frames.sort_values([0])
# print(frames.join(J,right_index=True))


J['index']=J.index
print(J)
print(frames)

frames['index']=frames.index


frames=frames.merge(J,on='index')
print(frames.columns)
frames=frames[['index','prob',1]]
frames.rename(index=str, columns={1: "BW"},inplace=True)

print(frames)
frames.to_csv('/Users/gaithrjoub/Desktop/pro/bwprobx.csv')