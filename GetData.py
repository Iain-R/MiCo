# -*- coding: utf-8 -*-

import csv
class Dataget:
    
    def __init__(self,poi_name,segment_name,distances_name):
        self.Data = []
        self.Seg=[]
        self.DistKM = {}
        self.poiFile = poi_name
        self.segFile = segment_name
        self.disFile = distances_name
        self.amountPoints = 0 
    
    
    def read_poi(self):
        """Gets you the co-ords for all poi, as given in the csv file """
        with open(self.poiFile, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if row[5]=="Latitude":
                    print("Getting Points of Interest")
                else:
                    self.Data.append((float(row[5]),float(row[6]),float(row[7])))
        self.amountPoints = len(self.Data)
        print("There are {} Points of Interest\n".format(self.amountPoints))
            


    def read_seg(self):
        """Finds the segment each POI is in, I think we should do this in here soon using Kmean"""
        with open(self.segFile, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                self.Seg.append((row[0]))
                    
        print("Segments now matched with Data points\n")
    
    def read_distances(self):
        """ I would like to also calculate the distances in the python code, to update """
        with open(self.disFile, newline='') as csvfile:
            j=-1
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                j+=1
                for i in range(len(row)):
                    self.DistKM[i,j]= float(row[i])
        print("Distnace Dictionary Complete")

    def SegmentSplit(self,Seg):
        self.read_poi()
        self.read_seg()
        self.read_distances()
        """Input the segment number that you want"""
        a = str(Seg)
        Seg1 = []
        seg1Dist = {}
        q= -1
        for i in range(self.amountPoints):
            if Seg[i]== a:
                #If this poi is in the selected segment 
                Seg1.append(self.Data[i])
                #Store the data of the point
                k = -1
                q+=1
                #calculate all distances
                for j in range(self.amountPoints):
                    if Seg[j] == a:
                        k+=1
                        if k<q:
                            seg1Dist[q,k] = self.DistKM[i,j]
        print("Data created for segment {}/n".format(Seg))
        return (Seg1,seg1Dist)
    def get_poi(self):
        return self.Data
    def get_distances(self):
        return self.DistKM
    def get_amount(self):
        return self.amountPoints
    def read_all(self):
        self.read_poi()
        self.read_distances()
        self.read_seg()

