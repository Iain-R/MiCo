# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 14:26:19 2018

@author: Iain
"""
import math
import random
import pylab
from tqdm import tqdm

class SimAnneal:
    
    def __init__(self,Data,pts):
        self.Data = Data 
        self.N = range(len(pts))
        self.nLoc = len(pts)
        self.Path = list(self.N)
        self.Pos = pts
        random.shuffle(self.Path)
        self.Randomcost = self.Cost()
            

    def Cost(self):
        return sum(self.Data[self.Path[i-1],self.Path[i]] for i in self.N)
    

    def ChooseNeigh(self):
        while True:
            i = random.choice(self.N)
            j = random.choice(self.N)
            if j<i:
                i,j = j,i
            if i!=j and j-1 < self.nLoc:
                break
        a1 = self.Path[i-1]
        a2 = self.Path[i]
        b1 = self.Path[j]    
        b2 = self.Path[(j+1)%self.nLoc]
        return self.Data[a1,b1]+self.Data[a2,b2]-(self.Data[a1,a2]+self.Data[b1,b2]),(i,j)

    def MoveToNeigh(self,neigh):
        i,j = neigh
        for k in range(int((j-i+1)/2)):
            self.Path[i+k],self.Path[j-k] = self.Path[j-k],self.Path[i+k] 
            
    def RunSA(self,run,T,alpha):
        E = self.Cost()
        Best = E
        CostArr = [E]
        BestArr = [Best]
        for i in tqdm(range(run),ascii = True, desc = "Simulated Annealing"):
            delta,neighbour = self.ChooseNeigh()
            if delta < 0 or random.random() < math.exp(-delta/T):
                self.MoveToNeigh(neighbour)
                E += delta
                if E < Best:
                    Best = E
            CostArr.append(E)
            BestArr.append(Best)
            T *= alpha
#        print (E)
        pylab.plot(range(run+1),CostArr)
        pylab.plot(range(run+1),BestArr)
        pylab.show()
        print("Total Distance Travelled is:", self.Cost())

    def printcost(self):
        print ("SA Cost:",self.Cost())
        print("Total Path = ", self.Cost()+(1.852**2)*math.pi*self.nLoc,'km')
        print('Flight Time = ', (self.Cost()+(1.852**2)*math.pi*self.nLoc)/(55*1.85),'hours')
        print("Random Walk", self.Randomcost)
        print(self.Cost()/self.Randomcost *100,"% Distance travelled compared to a random strategy")
        
    def getpath(self):
        return(self.Path)
    def printpath(self):
        print(self.Path)
    def Showroute(self):
        pylab.plot([self.Pos[self.Path[i]][0] for i in range(-1,self.nLoc)], [self.Pos[self.Path[i]][1] for i in range(-1,self.nLoc)])
        pylab.show()

    


