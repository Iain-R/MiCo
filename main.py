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
Seg1 = []

for i in Seg:
    if i == 1:
        Seg1.append(Data[i])



def Distance(p1,p2):
    
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def GetDist(Data):
    return [[Distance(Data[i],Data[j]) for j in range(len(Data))]for i in range(len(Data))]
    

A = SimAnneal(GetDist(Data),Data,False)
A.RunSA(1000000,90000,0.99995)
#A.RunSA(500000,50000,0.9998)
#A.printpath()
A.printcost()
A.Showroute()