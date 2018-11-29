# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 15:01:40 2018

@author: Iain
"""



"""

What about a resoource constrained DP ??
"""
from SAClass import SimAnneal
import math

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
            Seg.append(row)
    print("There are ",len(Data),"Points")
DistKM ={}
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


def Distance(p1,p2):
    
    return DistKM[p1,p2]

def GetDist(Data):
    return [[Distance(i,j) for j in range(len(Data))]for i in range(len(Data))]
    

A = SimAnneal(GetDist(Seg1),Seg1,False)
A.RunSA(1000000,90000,0.99995)
#A.RunSA(500000,50000,0.9998)
#A.printpath()
A.printcost()
A.Showroute()