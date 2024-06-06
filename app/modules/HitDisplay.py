# External Packages | NumPy
import numpy as np

# External Packages | pyqtgraph
import pyqtgraph as pg

from PyQt5.QtCore import Qt, QTimer, QObject
from PyQt5.QtWidgets import  QGridLayout



class HitDisplay(QObject):  # Inherit from QObject

    def __init__(self, elementid, detectorid, selectedEvents, sid, hits, eventID, track, layout):
        super().__init__()  # Call the constructor of QObject
        self.elementid = elementid
        self.detectorid = detectorid
        self.selectedEvents = selectedEvents
        self.sid = sid
        self.hits = hits
        self.eventID = eventID
        self.track = track
        #self.plot_widget = plot_widget
        self.layout = layout
        
        self.ith_event = 0
        # Create a grid layout for the scatter plots
        grid_layout = pg.GraphicsLayoutWidget()
        for i in range(3):
            for j in range(3):
                p = grid_layout.addPlot(row=i, col=j)
                self.display(p)
                self.ith_event += 1
        
        # Add the grid layout to the widget layout
        self.layout.addWidget(grid_layout)

    def display(self, plot_widget):
        scatter_raw = self.Raw_Hit()  
        scatter_cluster = self.Cluster_Hit()  
        scatter_mup, scatter_mum = self.Track_Hits()  

        plot_widget.addItem(scatter_raw)
        plot_widget.addItem(scatter_cluster)                 
        plot_widget.addItem(scatter_mup)
        plot_widget.addItem(scatter_mum)


         #Define the dictionary for x-axis labels
        x_labels = {
            (0, 5): "ST0",
            (12, 17): "ST2",
            (18, 23): "ST3m",
            (24, 29): "ST3P",
            (30, 33): "H1",
            (34, 37): "H2",
            (38, 39): "H3",
            (40, 45): "H4",
            (46, 54): "Prop"
        }

        # Create ticks for the x-axis
        ticks = []
        for (start, end), label in x_labels.items():
            mid = (start + end) / 2  # Position the label in the middle of the range
            ticks.append((mid, label))
        
        # Set the ticks for the x-axis
        plot_widget.getAxis('bottom').setTicks([ticks])

        # Set y-axis range to 0-201
        plot_widget.setLimits(yMin=0, yMax=201)





    #this isn't working yet...
    def normalize_y(self, data):
        x_values = data[:, 0]
        y_values = data[:, 1]
        
        # Get the indices where x is between 30 and 45
        mask = (x_values >= 18) & (x_values <= 54)
        
        # Normalize the y-values in this range
        y_values[mask] = 201 * (y_values[mask] - np.min(y_values[mask])) / (np.max(y_values[mask]) - np.min(y_values[mask]))
        
        # Return the updated data
        return np.column_stack((x_values, y_values))

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
        data = np.column_stack((self.detectorid[eventIndex][0], self.elementid[eventIndex][0]))
        #data = self.normalize_y(data)
        scatter = pg.ScatterPlotItem(pos=data, pen=pg.mkPen(None), symbol='o', size=10, brush=pg.mkBrush(128, 128, 128, 50))
        return scatter

    def Cluster_Hit(self):
        '''creates a scatter plot item of the hits after declustering from Qtracker'''
        eventIndex = np.where(self.selectedEvents[self.ith_event] == self.eventID)[0]
        cluster = np.vstack((np.where(self.hits[eventIndex]==True)[1], np.where(self.hits[eventIndex]==True)[2])).T
        #shift detector from 0 to 1
        cluster[:,0] = cluster[:,0]+1
        # Create a scatter plot item

        #data = self.normalize_y(cluster)
        scatter = pg.ScatterPlotItem(pos=cluster, pen=pg.mkPen(None), symbol='o', size=10, brush=pg.mkBrush(255, 255, 255, 80))
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

        data_mup = np.column_stack((detectorid_mup, elementid_mup))
        data_mum = np.column_stack((detectorid_mum, elementid_mum))

        #data_mup = self.normalize_y(data_mup)
        #data_mum = self.normalize_y(data_mum)

        scatter_mup = pg.ScatterPlotItem(pos = data_mup, pen=pg.mkPen(None), symbol='s', size=10, brush=pg.mkBrush(255, 0, 0, 120))
        scatter_mum = pg.ScatterPlotItem(pos = data_mum, pen=pg.mkPen(None), symbol='s', size=10, brush=pg.mkBrush(0, 255, 0, 120))

        return scatter_mup, scatter_mum
