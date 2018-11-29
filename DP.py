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
import sys 
sys.setrecursionlimit(4500)

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
nLoc = len()
N = range(len(Data))
print("Calculating {} points".format(nLoc))
Square = 100
#random.seed(nLoc)
Pos = [(random.randint(0,Square), random.randint(0,Square)) for i in N]
#Data = [[Distance(Seg1[i],Seg1[j]) for j in N] for i in N]
#Data = Distance
Path = list(N)

Cost = 0
path = []
def pt(current,remaining):
    global Cost
    global path
#    print(remaining)
    if len(remaining)==1:
        Cost+=DistKM[current,remaining[0]]
        return None
    nxt = remaining[0]
    Best = 100000000
    for i in remaining:
       if DistKM[current,i]<Best:
           Best = DistKM[current,i]
           nxt = i
    Cost+=Best
    path.append(current)
    remaining.remove(nxt)
    pt(nxt,remaining)
    
#pt(0,[1,2,3,4,5])
pt(0,list(N))
print(Cost+((1.852**2)*math.pi*nLoc))
print((Cost+((1.852**2)*math.pi*nLoc))/(55*1.85))
print("KM of Transit",Cost)
print("Time in Transit",Cost/(55*1.852))
pylab.plot([Data[path[i]][1] for i in range(-1,nLoc-1)], [Data[path[i]][0] for i in range(-1,nLoc-1)])
pylab.xlabel('Latitude(Degrees)')
pylab.ylabel('Longitude (Degrees)')
pylab.title('Greedy Technique')
pylab.show()



