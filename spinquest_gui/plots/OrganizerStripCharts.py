#strip charts for x,y,z vertices w.r.t event id

import sys
import os
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QApplication



# module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'calculations'))
# if module_path not in sys.path:
#     sys.path.append(module_path)

#from spinquest_gui.modules.calculations.DataReader import DataReader
from spinquest_gui.modules.calculations.DataOrganizer import DataOrganizer
from spinquest_gui.modules.directories.directory_health import get_reconstructed_directory

import pyqtgraph as pg

application = QApplication(sys.argv)

class OrgStripCharts(QWidget):

    def __init__(self, organizer : DataOrganizer):

        super().__init__()

        layout=QVBoxLayout()
        self.vtxPlot=pg.plot()
        self.vtyPlot=pg.plot()
        self.vtzPlot=pg.plot()
        self.txtin = QLineEdit(self)
        self.vtxPlot.showGrid(x=True,y=True)
        self.vtxPlot.setLabel('bottom',"Event ID")
        self.vtxPlot.setLabel('left',"X Vertex (cm)")
        self.vtyPlot.showGrid(x=True,y=True)
        self.vtyPlot.setLabel('bottom',"Event ID")
        self.vtyPlot.setLabel('left',"Y Vertex (cm)")
        self.vtzPlot.showGrid(x=True,y=True)
        self.vtzPlot.setLabel('bottom',"Event ID")
        self.vtzPlot.setLabel('left',"Z Vertex (cm)")
        layout.addWidget(self.txtin)
        layout.addWidget(self.vtxPlot)
        layout.addWidget(self.vtyPlot)
        layout.addWidget(self.vtzPlot)
        self.vtxSPlot=pg.plot()
        self.vtySPlot=pg.plot()
        self.vtzSPlot=pg.plot()
        self.vtxSPlot.showGrid(x=True,y=True)
        self.vtxSPlot.setLabel('bottom',"Spill ID")
        self.vtxSPlot.setLabel('left',"X Vertex (cm)")
        self.vtySPlot.showGrid(x=True,y=True)
        self.vtySPlot.setLabel('bottom',"Spill ID")
        self.vtySPlot.setLabel('left',"Y Vertex (cm)")
        self.vtzSPlot.showGrid(x=True,y=True)
        self.vtzSPlot.setLabel('bottom',"Spill ID")
        self.vtzSPlot.setLabel('left',"Z Vertex (cm)")
        layout.addWidget(self.vtxSPlot)
        layout.addWidget(self.vtySPlot)
        layout.addWidget(self.vtzSPlot)
        self.setLayout(layout)
        

        # if not (os.path.exists("event_vertex_data")):
        #     path = os.path.join("event_vertex_data")
        #     os.mkdir(path)
        #     with open("event_vertex_data/README.txt",'w') as README:
        #         README.write("This directory contains npz files which each contain 4 numpy arrays saved as npy files.\n")
        #         README.write("The 0th array contains event IDs.\n")
        #         README.write("The 1st, 2nd, and 3rd arrays contain X, Y, and Z vertex positions respectively.\n")
        #         README.write("The arrays are saved such that the Nth event ID corresponds to the Nth instance of vertex data.\n")

        # if not (os.path.exists("SpillVertexMeans")):
        #     path = os.path.join("SpillVertexMeans")
        #     os.mkdir(path)
        #     with open ("SpillVertexMeans/README.txt",'w') as README:
        #         README.write("This directory contains npz files labeled by spill. Each file contains 7 0-dimensional arrays stored in npy files\n")
        #         README.write("The 0th array contains the spill ID\n")
        #         README.write("The 1st, 2nd, and 3rd arrays contain the mean X, Y, and Z vertex positions over all events in the spill respectively\n")
        #         README.write("The 4th, 5th, and 6th arrays contain the standard deviations of X, Y, and Z vertex positions respectively\n")


        self.MAX_SPILLS = 5
        self.xScatter = []
        self.yScatter = []
        self.zScatter = []
        self.xSScatter = []
        self.ySScatter = []
        self.zSScatter = []
        self.xErr = []
        self.yErr = []
        self.zErr = []
        self.currentFile = 0
        self.position = 0
        self.spillsDisplayed = 0

        self.filenames = sorted([filename for filename in os.listdir(get_reconstructed_directory()) if filename.endswith(".npz")])
        self.fileCount = len(self.filenames)
        if (self.fileCount == 0 ):
            print("Your Reconstructed directory is empty, make sure the files from QTracker are being sent there\n")
        while (self.currentFile < self.fileCount):
            if (self.currentFile >= self.MAX_SPILLS):
                self.vtxPlot.removeItem(self.xScatter[self.position])
                self.vtyPlot.removeItem(self.yScatter[self.position])
                self.vtzPlot.removeItem(self.zScatter[self.position])
                self.vtxSPlot.removeItem(self.xSScatter[self.position])
                self.vtySPlot.removeItem(self.ySScatter[self.position])
                self.vtzSPlot.removeItem(self.zSScatter[self.position])
                self.vtxSPlot.removeItem(self.xErr[self.position])
                self.vtySPlot.removeItem(self.yErr[self.position])
                self.vtzSPlot.removeItem(self.zErr[self.position])
            self.DrawSpill(organizer)

    def UpdateChart(self, organizer : DataOrganizer):
        if (self.spillsDisplayed >= self.MAX_SPILLS):
            self.vtxPlot.removeItem(self.xScatter[self.position])
            self.vtyPlot.removeItem(self.yScatter[self.position])
            self.vtzPlot.removeItem(self.zScatter[self.position])
            self.vtxSPlot.removeItem(self.xSScatter[self.position])
            self.vtySPlot.removeItem(self.ySScatter[self.position])
            self.vtzSPlot.removeItem(self.zSScatter[self.position])
            self.vtxSPlot.removeItem(self.xErr[self.position])
            self.vtySPlot.removeItem(self.yErr[self.position])
            self.vtzSPlot.removeItem(self.zErr[self.position])
            self.DrawSpill(organizer)


    
    def DrawSpill(self, organizer : DataOrganizer):
        self.eidData = organizer.eid
        self.sidData = organizer.sid[0]
        self.vtxData = organizer.vtx
        self.vtyData = organizer.vty
        self.vtzData = organizer.vtz
        self.vtxMean = np.array([np.mean(self.vtxData)])
        self.vtyMean = np.array([np.mean(self.vtyData)])
        self.vtzMean = np.array([np.mean(self.vtzData)])
        self.vtxSTD = np.std(self.vtxData)
        self.vtySTD = np.std(self.vtyData)
        self.vtzSTD = np.std(self.vtzData)
        if (self.spillsDisplayed < self.MAX_SPILLS):
            self.xScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,0,255,255)))
            self.yScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(255,0,0,255)))
            self.zScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,255,0,255)))
            self.xSScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,0,255,255)))
            self.ySScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(255,0,0,255)))
            self.zSScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,255,0,255)))
            self.xErr.append(pg.ErrorBarItem(x=self.sidData,y=self.vtxMean,height=self.vtxSTD,pen=pg.mkPen(0,0,255,255),beam=0.5))
            self.yErr.append(pg.ErrorBarItem(x=self.sidData,y=self.vtyMean,height=self.vtySTD,pen=pg.mkPen(255,0,0,255),beam=0.5))
            self.zErr.append(pg.ErrorBarItem(x=self.sidData,y=self.vtzMean,height=self.vtzSTD,pen=pg.mkPen(0,255,0,255),beam=0.5))
            self.spillsDisplayed += 1
        self.xScatter[self.position].setData(self.eidData,self.vtxData)
        self.vtxPlot.addItem(self.xScatter[self.position])
        self.yScatter[self.position].setData(self.eidData,self.vtyData)
        self.vtyPlot.addItem(self.yScatter[self.position])
        self.zScatter[self.position].setData(self.eidData,self.vtzData)
        self.vtzPlot.addItem(self.zScatter[self.position])
        self.xErr[self.position] = pg.ErrorBarItem(x=self.sidData,y=self.vtxMean,height=self.vtxSTD,pen=pg.mkPen(0,0,255,255),beam=0.5)
        self.xSScatter[self.position].setData(self.sidData,self.vtxMean)
        self.vtxSPlot.addItem(self.xSScatter[self.position])
        self.vtxSPlot.addItem(self.xErr[self.position])
        self.yErr[self.position] = pg.ErrorBarItem(x=self.sidData,y=self.vtyMean,height=self.vtySTD,pen=pg.mkPen(255,0,0,255),beam=0.5)
        self.ySScatter[self.position].setData(self.sidData,self.vtyMean)
        self.vtySPlot.addItem(self.ySScatter[self.position])
        self.vtySPlot.addItem(self.yErr[self.position])
        self.zErr[self.position] = pg.ErrorBarItem(x=self.sidData,y=self.vtzMean,height=self.vtzSTD,pen=pg.mkPen(0,255,0,255),beam=0.5)
        self.zSScatter[self.position].setData(self.sidData,self.vtzMean)
        self.vtzSPlot.addItem(self.zSScatter[self.position])
        self.vtzSPlot.addItem(self.zErr[self.position])
        self.spillString = str(self.sidData)
        # np.savez(f'{get_event_vertex_data_directory()}{self.spillString}.npz', self.eidData,self.vtxData,self.vtyData,self.vtzData)
        # np.savez(f'{get_spill_vertex_means_directory()}{self.spillString}.npz', self.sidData,self.vtxMean,self.vtyMean,self.vtzMean,self.vtxSTD,self.vtySTD,self.vtzSTD)
        self.currentFile += 1
        self.position += 1
        self.position = self.position % self.MAX_SPILLS
        layout=self.layout()