# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 15:01:40 2018

@author: Iain
"""
import sys 
sys.path.insert(0, 'C:\gurobi810\win64\python37\lib')
import math
import random
import itertools
from gurobipy import *

import csv
Data = []
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
seg1Dist = {}
for i in range(len(Seg)):
#    print(i)
    if Seg[i]== '1':
        Seg1.append(Data[i])
        k = -1
        for j in range(len(Seg)):
           
            if Seg[j] == '1':
                k+=1
                seg1Dist[len(Seg1)-1,k] = DistKM[i,j]
n = int(len(Seg1))

def subtourelim(model, where):
    print('callback')
    if where == GRB.Callback.MIPSOL:
        # make a list of edges selected in the solution
        vals = model.cbGetSolution(model._vars)
        selected = tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
        # find the shortest cycle in the selected edge list
        tour = subtour(selected)
        if len(tour) < n:
            # add subtour elimination constraint for every pair of cities in tour
            model.cbLazy(quicksum(model._vars[i,j]
                                  for i,j in itertools.combinations(tour, 2))
                         <= len(tour)-1)

# Given a tuplelist of edges, find the shortest subtour

def subtour(edges):
    unvisited = list(range(n))
    cycle = range(n+1) # initial length has 1 more city
    while unvisited: # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i,j in edges.select(current,'*') if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle

n = int(len(Seg1))
print(n)
# Create n random points

dist = seg1Dist 
m = Model()

# Create variables

vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
for i,j in vars.keys():
    vars[j,i] = vars[i,j] # edge in opposite direction


# Add degree-2 constraint
m.addConstrs(vars.sum(i,'*') == 2 for i in range(n))


# Optimize model

m._vars = vars
m.Params.lazyConstraints = 1
m.optimize(subtourelim)

vals = m.getAttr('x', vars)
selected = tuplelist((i,j) for i,j in vals.keys() if vals[i,j] > 0.5)

tour = subtour(selected)
print(len(tour))
assert len(tour) == n

print('')
print('Optimal tour: %s' % str(tour))
print('Optimal cost: %g' % m.objVal)
print('')
