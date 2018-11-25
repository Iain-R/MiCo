# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 11:24:20 2018

@author: Iain
"""


import sys 
sys.path.insert(0, 'C:\gurobi810\win64\python37\lib')
import math
import random
import itertools
from gurobipy import *

Flight = 2

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
with open('32seg.csv', newline='') as csvfile:
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

def SegmentSplit(a):
    a = str(a)
    Seg1 = []
    seg1Dist = {}
    q= -1
    for i in range(len(Seg)):
    #    print(i)
        if Seg[i]== a:
            Seg1.append(Data[i])
            k = -1
            q+=1
            for j in range(len(Seg)):
                if Seg[j] == a:
                    k+=1
                    if k<q:
    #                    print(q,k)      
                        seg1Dist[q,k] = DistKM[i,j]
    return (Seg1,seg1Dist)

for i in range(31):
    Flight = i+1
    n = int(len(SegmentSplit(Flight)[0]))
    
    seg1Dist = SegmentSplit(Flight)[1]
    Seg1 = SegmentSplit(Flight)[0]
    
    # Callback - use lazy constraints to eliminate sub-tours
    def subtourelim(model, where):
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
    assert len(tour) == n
    
    print('Route Planned')
    print('Optimal tour: %s' % str(tour))
    print('Optimal cost: %g' % m.objVal)
    print('Time : ',(m.objVal+(n*(math.pi*(1.852**2))))/(1.85*55))
    print('')
    output = []
    for i in tour:
        output.append(Seg1[i])
    import json
    with open('Flight{}.json'.format(Flight), 'w') as outfile:
        a = []
        for i in output:
            a.append({"Longitude" : str(i[1]) ,"Latitude" : str(i[0]) })
            
    #       json.dump({"Longitude" : str(i[0]) ,"Latitude" : str(i[1]) },outfile)
        json.dump(a,outfile)