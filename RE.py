# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 11:24:20 2018

@author: Iain
"""
import sys 
sys.path.insert(0, 'C:\gurobi810\win64\python37\lib')
import math
import itertools
from gurobipy import *
import pylab
from GetData import Dataget


Files = Dataget('poi.csv','32seg.csv','distances.csv')
Files.read_all()
Distance = Files.get_distances()
Data = Files.get_poi()
COST = 0
TIME = 0
for i in range(31):
    Flight = i+1
    n = int(len(Files.SegmentSplit(Flight)[0]))
    seg1Dist = Files.SegmentSplit(Flight)[1]
    Seg1 = Files.SegmentSplit(Flight)[0]
    
#    print(Seg1)
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
    print('Time in Transit', m.objVal/(1.85*55))
    print('Optimal Distance',(m.objVal+(n*(math.pi*(1.852**2)))))
    COST+=m.objVal
    TIME +=  m.objVal/(1.85*55)
    print('Time : ',(m.objVal+(n*(math.pi*(1.852**2))))/(1.85*55))
    print('')
    output = []
    for i in tour:
        output.append(Seg1[i])
    import json
    
    with open('Flight{}seg32.json'.format(Flight), 'w') as outfile:
        a = [{"Longitude" : "151.8029","Latitude" : "-25.0138"}]
        
        for i in output:
            
            a.append({"Longitude" : str(i[1]) ,"Latitude" : str(i[0]) })
            
#           json.dump({"Longitude" : str(i[0]) ,"Latitude" : str(i[1]) },outfile)
        json.dump(a,outfile)
#    pylab.plot([Seg1[tour[i]][1] for i in range(-1,n-1)], [Seg1[tour[i]][0] for i in range(-1,n-1)])
#    pylab.xlabel('Latitude(Degrees)')
#    pylab.ylabel('Longitude (Degrees)')
#    pylab.title('MIP Technique')
##    pylab.show()
