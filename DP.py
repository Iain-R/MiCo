# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 21:21:00 2018

@author: Iain
"""

#def Distance():
#    
#    return 9
#mem={}
#def DP(state, stage,Time):
#    if Time <= dist(stage,home):
#        DP()
#    if (state,stage) not in mem:
#        mem[state,stage] = min(for a in stage)
    
    
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


def Distance(p1, p2):
    """Calculates the Distance between two points Distance(p1,p2)--> R"""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
#This just 
nLoc = 100
N = range(nLoc)
Square = 100
random.seed(nLoc)
Pos = [(random.randint(0,Square), random.randint(0,Square)) for i in N]
Data = [[Distance(Pos[i],Pos[j]) for j in N] for i in N]
Path = list(N)

_D={}
def D(stage,state,pred):
    print(stage)
    if stage <= 0:
        print("DONE")
        return Data[state][0]
        
    if (stage,state) not in _D:
        _D[stage,state] = min(Data[state][a] + D(stage-1,a,pred+[state]) for a in N if a not in pred and a != stage)
    
    return _D[stage,state] 


def TSP(G,N):
    for k in range(2,N):
        