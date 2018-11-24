# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 15:25:00 2018

@author: Iain
"""

Data = []
import csv
with open('poi.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        Data.append((row[5],row[6],row[7]))
    print("There are ",len(Data),"Points")
        

