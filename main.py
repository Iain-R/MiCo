# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 15:01:40 2018

@author: Iain
"""
#What about a resoource constrained DP ??
from SAClass import SimAnneal
from GetData import Dataget
Files = Dataget('poi.csv','32seg.csv','distances.csv')
Files.read_all()

print("Calculating {} points Using Simulated Annealing".format(Files.get_amount()))

Distance = Files.get_distances()
Data = Files.get_poi()

A = SimAnneal(Distance,Data)
A.RunSA(1000000,90000,0.99995)

A.printcost()
A.Showroute()