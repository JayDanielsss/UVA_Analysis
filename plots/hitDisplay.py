# Native Package | sys
import sys

# External Packages | NumPy
import numpy as np


# External Packages | pyqtgraph
import pyqtgraph as pg

class HitDisplay:
    def __init__(self):
        #elemid =np.where(hits==True)[1]
        #detid = np.where(hits==True)[0]
        
        
        print("HitDisplay")
        
        

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
        
        

        for i in range(30,46):
            Hodo[30-i] = len(hitmatrix[(hitmatrix[:,0]==i)])
            
        for i in range(46,54):
            propTube[46-i] = len(hitmatrix[(hitmatrix[:,0]==i)])
            


        
        
        return(hitmatrix, DC, Hodo, propTube)


        
        #Occ = [count_st1,count_st2,count_st3,count_st4]
        
        #return Occ
    


    def Raw_Hit(self, elementid, detectorid, selectedEvents, sid, eventID):
        eventIndex = np.where(selectedEvents[0] == eventID)[0]
        # Create a scatter plot item
        scatter = pg.ScatterPlotItem(detectorid[eventIndex][0],elementid[eventIndex][0], pen=pg.mkPen(None), symbol='o', size=10, brush=pg.mkBrush(128, 128, 128, 50))
        return scatter
    def Cluster_Hit(self,hits, selectedEvents, sid, eventID):
        eventIndex = np.where(selectedEvents[0] == eventID)[0]
        cluster = np.vstack((np.where(hits[eventIndex]==True)[1],np.where(hits[eventIndex]==True)[2])).T
        #shift detector from 0 to 1
        cluster[:,0] = cluster[:,0]+1
        # detectorid = np.arange(0,55)
        # print(elementID)
        
        # # Create a scatter plot item
        scatter = pg.ScatterPlotItem(cluster[:,0],cluster[:,1], pen=pg.mkPen(None), symbol='o', size=10, brush=pg.mkBrush(255, 255, 255, 80))
        return scatter
    def Track_Hits(self,selectedEvents,sid,eventID,track):
        elementid_mup = track[0][:34,0]
        elementid_mum = track[0][34:,0]
        st1 = np.arange(1,7)
        st2 = np.arange(13,19)
        st3m = np.arange(19,25)
        st3p = np.arange(25,31)
        hodo = np.arange(31,39) 
        prop = np.arange(47,55)
        if elementid_mup[13] > 0:
            detectorid_mup = np.concatenate((st1,st2,st3p,hodo,prop))
        else:
            detectorid_mup = np.concatenate((st1,st2,st3m,hodo,prop))

        if elementid_mum[13] > 0:
            detectorid_mum = np.concatenate((st1,st2,st3p,hodo,prop))
        else:
            detectorid_mum = np.concatenate((st1,st2,st3m,hodo,prop))

        elementid_mup = np.abs(elementid_mup)
        elementid_mum = np.abs(elementid_mum)

        scatter_mup = pg.ScatterPlotItem(detectorid_mup,elementid_mup, pen=pg.mkPen(None), symbol='s', size=10, brush=pg.mkBrush(255, 0, 0, 120))
        scatter_mum = pg.ScatterPlotItem(detectorid_mum,elementid_mum, pen=pg.mkPen(None), symbol='s', size=10, brush=pg.mkBrush(0, 255, 0, 120))

        return scatter_mup, scatter_mum

        
# import time
# from DataOrganizer import dataOrganizer

# #Testing
# t0 = time.time()
#  #Create an instance of dataOrganizer
# organizer = dataOrganizer()

# # Call the organizeData() method to populate the necessary attributes
# organizer.organizeData()

# # Call the organizeData() method on the instance

# elementid, detectorid, selectedEvents, sid, hits, eventID, track= organizer.grab_HitInfo()
# hitmatrices = HitDisplay()
# scatter_raw = hitmatrices.Raw_Hit(elementid,detectorid, selectedEvents, sid, eventID)
# scatter_cluster = hitmatrices.Cluster_Hit(hits,selectedEvents,sid,eventID)
# scatter_mup, scatter_mum = hitmatrices.Track_Hits(selectedEvents,sid,eventID,track)




# # # # Create the PyQtGraph application
# app = QApplication(sys.argv)

# # Create a window
# win = pg.GraphicsLayoutWidget(show=True, title="Scatter Plot Example")
# win.resize(800, 600)
# win.setWindowTitle('pyqtgraph example: Scatter Plot')

# # Enable antialiasing for prettier plots
# pg.setConfigOptions(antialias=True)

# # Create a plot item
# plot = win.addPlot()


# # Add the scatter plot item to the plot
# plot.addItem(scatter_raw)
# plot.addItem(scatter_cluster)
# plot.addItem(scatter_mup)
# plot.addItem(scatter_mum)

# t1 = time.time()

# total = t1 - t0
# print(total)


# sys.exit(app.exec_())








