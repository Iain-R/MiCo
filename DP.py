# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 21:21:00 2018

@author: Iain
"""
import time
starttime = time.time()

"""
State -> Amount of time left, if this is less than distance to home then you must return home
Stage -> Nodes left unvisited 
Action -> Move from Node i to j 
Transfer -> going from i to j removes j from the list of untravelled nodes and removes Dist(i,j)
from the state      
End Condition -> All nodes visited 
"""
import math
import random
import pylab


Data = []
import csv
with open('poi.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[5]=="Latitude":
            print("Starting Scrape")
        else:
            Data.append((float(row[5]),float(row[6]),float(row[7])))
    print("There are ",len(Data),"Points")


Seg = []
with open('8seg.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[0]=="Latitude":
            print("Starting Scrape")
        else:
#            print(row[0])
            Seg.append((row[0]))
            
    print("There are ",len(Data),"Points")
    
    
DistKM = {}
with open('distances.csv', newline='') as csvfile:
    j=-1
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        j+=1
        if row[0]=="Latitude":
            print("Starting Scrape")
        else:
#            print(row[0])
            for i in range(len(row)):
                DistKM[i,j]= float(row[i])
#                print(float(row[i]))
print(DistKM[0,0])
            
Seg1 = []
for i in range(len(Seg)):
#    print(i)
    if Seg[i]== '1':
        Seg1.append(Data[i])
#        for j in range(len(Seg1)):
#            seg1Dist[i,j]:

def Distance(p1, p2):
    """Calculates the Distance between two points Distance(p1,p2)--> R"""
    
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
#This just 
nLoc = len(Seg1)
N = range(len(Seg1))
print("Calculating {} points".format(nLoc))
Square = 100
#random.seed(nLoc)
Pos = [(random.randint(0,Square), random.randint(0,Square)) for i in N]
Data = [[Distance(Seg1[i],Seg1[j]) for j in N] for i in N]
#Data = Distance
Path = list(N)

_D={}



def D(stage,state,pred):
#    print(stage)
    if stage <= 1:
#        print("DONE")
        return (Data[state][0],state,0)
        
    if (stage,state,frozenset(pred)) not in _D:
        _D[stage,state,frozenset(pred)] = min((Data[state][a] + D(stage-1,a,pred+[state])[0],state,a) for a in N if a not in pred and a != state)
    return _D[stage,state,frozenset(pred)] 

#_memo = {}
#def ReFuel(Fuel,Position,Pred):
#    if Fuel<=time(Position,0):
#        return (DistKM[Position,0],Position,0,Fuel)
#    if (Fuel,Position,frozenset(Pred)) not in _memo:
#        
#        


print(D(10,0,[0]))
print(time.time()-starttime,'seconds')
