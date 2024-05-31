# External Packages | NumPy
import numpy as np

# External Packages | pyqtgraph
import pyqtgraph as pg

from PyQt5.QtCore import Qt, QTimer, QObject

class HitDisplay(QObject):  # Inherit from QObject

    def __init__(self, elementid, detectorid, selectedEvents, sid, hits, eventID, track, plot_widget):
        super().__init__()  # Call the constructor of QObject
        self.elementid = elementid
        self.detectorid = detectorid
        self.selectedEvents = selectedEvents
        self.sid = sid
        self.hits = hits
        self.eventID = eventID
        self.track = track  
        self.plot_widget = plot_widget  

        self.ith_event = 0 
        #timer to cycle through events
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display)  
        self.timer.start(1000)  # Call hit_display every 1000 milliseconds (1 second)

        if self.ith_event >= len(self.selectedEvents):
            self.timer.stop()
            return

    def display(self):
        #display pyqtgraph setup 
        if self.ith_event >= len(self.selectedEvents):
            self.timer.stop()
            return
        scatter_raw = self.Raw_Hit()  
        scatter_cluster = self.Cluster_Hit()  
        scatter_mup, scatter_mum = self.Track_Hits()  

        # Clear the plot widget before drawing new data
        self.plot_widget.clear()
        # Add the scatter plot items to the plot widget
        self.plot_widget.addItem(scatter_raw)
        self.plot_widget.addItem(scatter_cluster)                 
        self.plot_widget.addItem(scatter_mup)
        self.plot_widget.addItem(scatter_mum)

        
        self.plot_widget.setYRange(0, 201)

        # Advance the event index
        self.ith_event += 1

    def getOcc(self, hits, selectedEvents, eventID, ith_event):
        '''Gets occupancy for each detector and percentages'''

        eventIndex = np.where(selectedEvents[ith_event] == eventID)[0]

        Hodo = np.zeros(16)

        DC = np.zeros(30)

        propTube = np.zeros(7)

        hitmatrix = np.vstack((np.where(hits[eventIndex]==True)[1],np.where(hits[eventIndex]==True)[2])).T
        #shift detector from 0 to 1
        hitmatrix[:,0] = hitmatrix[:,0]+1

        for i in range(1,7):
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
            
        return (DC, Hodo, propTube)

    def Raw_Hit(self):
        '''creates a scatter plot item of the raw hits from the detector'''
        eventIndex = np.where(self.selectedEvents[self.ith_event] == self.eventID)[0]
        # Create a scatter plot item
        scatter = pg.ScatterPlotItem(self.detectorid[eventIndex][0], self.elementid[eventIndex][0], pen=pg.mkPen(None), symbol='o', size=10, brush=pg.mkBrush(128, 128, 128, 50))
        return scatter

    def Cluster_Hit(self):
        '''creates a scatter plot item of the hits after declustering from Qtracker'''
        eventIndex = np.where(self.selectedEvents[self.ith_event] == self.eventID)[0]
        cluster = np.vstack((np.where(self.hits[eventIndex]==True)[1], np.where(self.hits[eventIndex]==True)[2])).T
        #shift detector from 0 to 1
        cluster[:,0] = cluster[:,0]+1
        # Create a scatter plot item
        scatter = pg.ScatterPlotItem(cluster[:,0], cluster[:,1], pen=pg.mkPen(None), symbol='o', size=10, brush=pg.mkBrush(255, 255, 255, 80))
        return scatter

    def Track_Hits(self):
        '''A scatter plot of the tracks selected by QTracker'''
        elementid_mup = self.track[self.ith_event][:34,0]
        elementid_mum = self.track[self.ith_event][34:,0]
        st1 = np.arange(1,7)
        st2 = np.arange(13,19)
        st3m = np.arange(19,25)
        st3p = np.arange(25,31)
        hodo = np.arange(31,39)
        prop = np.arange(47,55)
        if elementid_mup[13] > 0:
            detectorid_mup = np.concatenate((st1, st2, st3p, hodo, prop))
        else:
            detectorid_mup = np.concatenate((st1, st2, st3m, hodo, prop))

        if elementid_mum[13] > 0:
            detectorid_mum = np.concatenate((st1, st2, st3p, hodo, prop))
        else:
            detectorid_mum = np.concatenate((st1, st2, st3m, hodo, prop))

        elementid_mup = np.abs(elementid_mup)
        elementid_mum = np.abs(elementid_mum)

        scatter_mup = pg.ScatterPlotItem(detectorid_mup, elementid_mup, pen=pg.mkPen(None), symbol='s', size=10, brush=pg.mkBrush(255, 0, 0, 120))
        scatter_mum = pg.ScatterPlotItem(detectorid_mum, elementid_mum, pen=pg.mkPen(None), symbol='s', size=10, brush=pg.mkBrush(0, 255, 0, 120))

        return scatter_mup, scatter_mum
