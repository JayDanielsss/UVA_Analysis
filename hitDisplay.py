import numpy as np
from DataReader import DataReader
import sys
import os
import matplotlib.pyplot as plt
from matplotlib import colors
import math

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys

class HitDisplay:
    def __init__(self, hits):
        #elemid =np.where(hits==True)[1]
        #detid = np.where(hits==True)[0]
        
        
        print("HitDisplay")
        
    def simpleHit(self,st,hitmatrix):
        geometery = np.loadtxt("geometery.csv", delimiter=",", dtype=str)
        

        def xCorrdinate(Plane,elemId,prime):
                z0 = float(geometery[Plane][-4])

                primePlane = Plane + prime
                z0P = float(geometery[primePlane][-4])
                planeDistance = round(abs(z0 - z0P),3)

                if(prime != 0):
                    Center = round(2*float(geometery[primePlane][5]),3)
                    xCorr = (elemId - ((float(geometery[primePlane][1])+1)/2))*float(geometery[primePlane][3]) + Center

                   # print((xCorr,(elemId-((float(geometery[primePlane][1])+1)/2))*float(geometery[primePlane][3])+ Center))
                else:
                    Center = round(float(geometery[Plane][8])+float(geometery[Plane][5]),3)
                    xCorr = (elemId - ((float(geometery[Plane][1])+1)/2))*float(geometery[Plane][3]) + Center
                    #print((xCorr,(elemId-((float(geometery[primePlane][1])+1)/2))*float(geometery[primePlane][3]) + Center))
                return xCorr

        if st == 1:
            VIndex = 0
            XIndex = 2
            UIndex = 4

            V = 0
            X = 2
            U = 4

            xZ = 623
            vZ = 597
            uZ = 648
            
            xHits = hitmatrix[hitmatrix[:,0]==X]
            xPHits = hitmatrix[hitmatrix[:,0]==X+1]

            xCorr=[]
            for i in range(len(xHits[:,1])):
                xCorr =np.append(xCorr,xCorrdinate(XIndex, xHits[i,1],prime=0))
            
            
            xPCorr=[]
            for i in range(len(xPHits[:,1])):
                xPCorr = np.append(xPCorr,xCorrdinate(XIndex+1, xPHits[i,1],prime=1))

            #clean memeory
            del xHits, xPHits

            
            #V hits

            vHits = hitmatrix[hitmatrix[:,0]==V]
            vPHits = hitmatrix[hitmatrix[:,0]==V+1]

            vCorr=[]
            for i in range(len(vHits[:,1])):
                vCorr =np.append(vCorr,xCorrdinate(VIndex, vHits[i,1],prime=0))
            
            
            vPCorr=[]
            for i in range(len(vPHits[:,1])):
                vPCorr =np.append(vPCorr,xCorrdinate(VIndex, vPHits[i,1],prime=1))

            
            del vHits, vPHits

            uHits = hitmatrix[hitmatrix[:,0]==U]
            uPHits = hitmatrix[hitmatrix[:,0]==U+1]

            uCorr=[]
            for i in range(len(uHits[:,1])):
                uCorr =np.append(uCorr,xCorrdinate(UIndex, uHits[i,1],prime=0))
            
            
            uPCorr=[]
            for i in range(len(uPHits[:,1])):
                uPCorr =np.append(uPCorr,xCorrdinate(UIndex, uPHits[i,1],prime=1))

            
            del uHits, uPHits


 
            xCorr = np.concatenate((xCorr,xPCorr))
            xCorr = np.column_stack((np.full(len(xCorr),xZ),xCorr))

            vCorr = np.concatenate((vCorr,vPCorr))
            vCorr = np.column_stack((np.full(len(vCorr),vZ),vCorr))
            
            uCorr = np.concatenate((uCorr,uPCorr))
            uCorr = np.column_stack((np.full(len(uCorr),uZ),uCorr))

            simpleHits = np.concatenate((vCorr,xCorr,uCorr))

            return(simpleHits)
        
        if st == 2:
            VIndex = 21
            XIndex = 24
            UIndex = 25

            V = 12
            X = 15
            U = 16

            xZ = 1327
            vZ = 1314
            uZ = 1365
            
            xHits = hitmatrix[hitmatrix[:,0]==X]
            xPHits = hitmatrix[hitmatrix[:,0]==X-1]

            xCorr=[]
            for i in range(len(xHits[:,1])):
                xCorr =np.append(xCorr,xCorrdinate(XIndex, xHits[i,1],prime=0))
            
            
            xPCorr=[]
            for i in range(len(xPHits[:,1])):
                xPCorr = np.append(xPCorr,xCorrdinate(XIndex-1, xPHits[i,1],prime=-1))

            #clean memeory
            del xHits, xPHits

            
            #V hits

            vHits = hitmatrix[hitmatrix[:,0]==V]
            vPHits = hitmatrix[hitmatrix[:,0]==V+1]

            vCorr=[]
            for i in range(len(vHits[:,1])):
                vCorr =np.append(vCorr,xCorrdinate(VIndex, vHits[i,1],prime=0))
            
            
            vPCorr=[]
            for i in range(len(vPHits[:,1])):
                vPCorr =np.append(vPCorr,xCorrdinate(VIndex, vPHits[i,1],prime=1))

            
            del vHits, vPHits

            uHits = hitmatrix[hitmatrix[:,0]==U]
            uPHits = hitmatrix[hitmatrix[:,0]==U+1]

            uCorr=[]
            for i in range(len(uHits[:,1])):
                uCorr =np.append(uCorr,xCorrdinate(UIndex, uHits[i,1],prime=0))
            
            
            uPCorr=[]
            for i in range(len(uPHits[:,1])):
                uPCorr =np.append(uPCorr,xCorrdinate(UIndex, uPHits[i,1],prime=1))

            
            del uHits, uPHits


 
            xCorr = np.concatenate((xCorr,xPCorr))
            xCorr = np.column_stack((np.full(len(xCorr),xZ),xCorr))

            vCorr = np.concatenate((vCorr,vPCorr))
            vCorr = np.column_stack((np.full(len(vCorr),vZ),vCorr))
            
            uCorr = np.concatenate((uCorr,uPCorr))
            uCorr = np.column_stack((np.full(len(uCorr),uZ),uCorr))

            simpleHits = np.concatenate((vCorr,xCorr,uCorr))

            return(simpleHits)


        if st == 3:
            VIndex = 36
            XIndex = 38
            UIndex = 40

            V = 19
            X = 21
            U = 23

            xZ = 1894
            vZ = 1888
            uZ = 1900
            
            xHits = hitmatrix[hitmatrix[:,0]==X]
            xPHits = hitmatrix[hitmatrix[:,0]==X-1]

            xCorr=[]
            for i in range(len(xHits[:,1])):
                xCorr =np.append(xCorr,xCorrdinate(XIndex, xHits[i,1],prime=0))
            
            
            xPCorr=[]
            for i in range(len(xPHits[:,1])):
                xPCorr = np.append(xPCorr,xCorrdinate(XIndex, xPHits[i,1],prime=-1))

            #clean memeory
            del xHits, xPHits

            
            #V hits

            vHits = hitmatrix[hitmatrix[:,0]==V]
            vPHits = hitmatrix[hitmatrix[:,0]==V-1]

            vCorr=[]
            for i in range(len(vHits[:,1])):
                vCorr =np.append(vCorr,xCorrdinate(VIndex, vHits[i,1],prime=0))
            
            
            vPCorr=[]
            for i in range(len(vPHits[:,1])):
                vPCorr =np.append(vPCorr,xCorrdinate(VIndex, vPHits[i,1],prime=-1))

            
            del vHits, vPHits

            uHits = hitmatrix[hitmatrix[:,0]==U]
            uPHits = hitmatrix[hitmatrix[:,0]==U-1]

            uCorr=[]
            for i in range(len(uHits[:,1])):
                uCorr =np.append(uCorr,xCorrdinate(UIndex, uHits[i,1],prime=0))
            
            
            uPCorr=[]
            for i in range(len(uPHits[:,1])):
                uPCorr =np.append(uPCorr,xCorrdinate(UIndex, uPHits[i,1],prime=-1))

            
            del uHits, uPHits


 
            xCorr = np.concatenate((xCorr,xPCorr))
            xCorr = np.column_stack((np.full(len(xCorr),xZ),xCorr))

            vCorr = np.concatenate((vCorr,vPCorr))
            vCorr = np.column_stack((np.full(len(vCorr),vZ),vCorr))
            
            uCorr = np.concatenate((uCorr,uPCorr))
            uCorr = np.column_stack((np.full(len(uCorr),uZ),uCorr))

            simpleHits = np.concatenate((vCorr,xCorr,uCorr))

            return(simpleHits)
        
        if st == 4:
            VIndex = 42
            XIndex = 44
            UIndex = 46

            V = 25
            X = 27
            U = 29

            xZ = 1931
            vZ = 1925
            uZ = 1937
            
            xHits = hitmatrix[hitmatrix[:,0]==X]
            xPHits = hitmatrix[hitmatrix[:,0]==X-1]

            xCorr=[]
            for i in range(len(xHits[:,1])):
                xCorr =np.append(xCorr,xCorrdinate(XIndex, xHits[i,1],prime=0))
            
            
            xPCorr=[]
            for i in range(len(xPHits[:,1])):
                xPCorr = np.append(xPCorr,xCorrdinate(XIndex, xPHits[i,1],prime=-1))

            #clean memeory
            del xHits, xPHits

            
            #V hits

            vHits = hitmatrix[hitmatrix[:,0]==V]
            vPHits = hitmatrix[hitmatrix[:,0]==V-1]

            vCorr=[]
            for i in range(len(vHits[:,1])):
                vCorr =np.append(vCorr,xCorrdinate(VIndex, vHits[i,1],prime=0))
            
            
            vPCorr=[]
            for i in range(len(vPHits[:,1])):
                vPCorr =np.append(vPCorr,xCorrdinate(VIndex, vPHits[i,1],prime=-1))

            
            del vHits, vPHits

            uHits = hitmatrix[hitmatrix[:,0]==U]
            uPHits = hitmatrix[hitmatrix[:,0]==U-1]

            uCorr=[]
            for i in range(len(uHits[:,1])):
                uCorr =np.append(uCorr,xCorrdinate(UIndex, uHits[i,1],prime=0))
            
            
            uPCorr=[]
            for i in range(len(uPHits[:,1])):
                uPCorr =np.append(uPCorr,xCorrdinate(UIndex, uPHits[i,1],prime=-1))

            
            del uHits, uPHits


 
            xCorr = np.concatenate((xCorr,xPCorr))
            xCorr = np.column_stack((np.full(len(xCorr),xZ),xCorr))

            vCorr = np.concatenate((vCorr,vPCorr))
            vCorr = np.column_stack((np.full(len(vCorr),vZ),vCorr))
            
            uCorr = np.concatenate((uCorr,uPCorr))
            uCorr = np.column_stack((np.full(len(uCorr),uZ),uCorr))

            simpleHits = np.concatenate((vCorr,xCorr,uCorr))

            return(simpleHits)


        
        else:
            print("Error")

    def headOnDisplay(self,hitmatrix):
        return(print("AHDSUGD"))

        

    def getOcc(self,hits,event):

        Hodo = np.zeros(15)

        DC = np.zeros(24)

        propTube = np.zeros(7)



        hitmatrix = np.vstack((np.where(hits[event]==True)[0],np.where(hits[event]==True)[1])).T

        for i in range(0,7):
            index = hitmatrix[hitmatrix[:,0] == i]
            DC[i] = len(index)

        for i in range(12,17):
            index = hitmatrix[hitmatrix[:,0] == i]
            DC[i-6] = len(index)
        
        for i in range(18,23):
            index = hitmatrix[hitmatrix[:,0] == i]
            DC[i-6] = len(index)
        for i in range(24,29):
            index = hitmatrix[hitmatrix[:,0] == i]
            DC[i-6] = len(index)
        
        # index1 = hitmatrix[(hitmatrix[:,0]>=0)*(hitmatrix[:,0]<=6)]
        
        # DC[0]= len(index1)


        
        # index1 = hitmatrix[(hitmatrix[:,0]>=12)*(hitmatrix[:,0]<=17)]
        
        # DC[1] = len(index1)
        
        # index1 = hitmatrix[(hitmatrix[:,0]>=18)*(hitmatrix[:,0]<=23)]
        
        # DC[2] = len(index1)

        # index1 = hitmatrix[(hitmatrix[:,0]>=24)*(hitmatrix[:,0]<=29)]
        
        # DC[3] = len(index1)

        #hodo occupancy

        for i in range(30,46):
            Hodo[30-i] = len(hitmatrix[(hitmatrix[:,0]==i)])
            
        for i in range(46,54):
            propTube[46-i] = len(hitmatrix[(hitmatrix[:,0]==i)])
            


        
        
        return(hitmatrix, DC, Hodo, propTube)


        
        #Occ = [count_st1,count_st2,count_st3,count_st4]
        
        #return Occ
    








filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"HIT")
plot_data = data_reader.read_data()
hits = plot_data[1]
eventID = plot_data[0]

print(hits)


# hitmatrix = np.vstack((np.where(hits==True)[0],np.where(hits==True)[1])).T
#print(hitmatrix)
# elemid =np.where(hits[0]==True)[1]
# detid = np.where(hits[0]==True)[0]
# plt.xlim(-1,7)
# plt.scatter(detid, elemid,marker='_')

# #plt.show()
# num_events = 20 #len(hits)
# hitmatrix = np.zeros((num_events,1000,2))

# DriftChamber = np.zeros((num_events,4))
# Hodoscope = np.zeros((num_events,15))
# propTube = np.zeros((num_events,7))

# #print(Hodoscope[0])

# for i in range(num_events):
#     hitM, DC, Hodo, Prop = HitDisplay.getOcc(hits, event=i)
#     padded_hitM = np.zeros((1000, 2))
#     padded_hitM[:hitM.shape[0], :] = hitM
#     hitmatrix[i] = padded_hitM
    
#     DriftChamber[i] = DC
#     Hodoscope[i] = Hodo
#     propTube[i] = Prop
    



# plt.scatter(hitmatrix[3][:,0],hitmatrix[3][:,1])
# #plt.xlim(44,60)
# plt.show()
# #print(len(np.where(hitmatrix[:,0]<=29)[0]))

# test1 = HitDisplay.simpleHit(hits,st=1,hitmatrix = hitmatrix[0])
# test2 = HitDisplay.simpleHit(hits,st=2,hitmatrix = hitmatrix[0])
# test3 = HitDisplay.simpleHit(hits,st=3,hitmatrix = hitmatrix[0])
# test4 = HitDisplay.simpleHit(hits,st=4,hitmatrix = hitmatrix[0])

# test = np.concatenate((test1,test2))
# test = np.concatenate((test,test3))
# test = np.concatenate((test,test4))


# plt.scatter(test[:,0],test[:,1])
# #plt.show()



# z_coords = test[:, 0]
# x_coords = test[:, 1]

# # Creating a heatmap
# plt.figure(figsize=(8, 6))
# #gridsize controls resolution
# plt.hexbin(x_coords, z_coords, gridsize=30, cmap='jet')
# plt.colorbar(label='hits')
# plt.xlabel('x-coordinate')
# #plt.xlim(-150,150)
# plt.ylabel('z-coordinate')
# plt.title('Heatmap of Hits in zx Plane')
# #plt.show()



