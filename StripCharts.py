#strip charts for x,y,z vertices w.r.t event id

import sys
import os
import numpy as np
import time
from pyqtgraph.Qt import QtGui
from random import randrange, uniform
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from DataReader import DataReader
import pyqtgraph as pg

class StripCharts(QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout()
        self.vtxPlot=pg.plot()
        self.vtyPlot=pg.plot()
        self.vtzPlot=pg.plot()
        self.txtin = QLineEdit(self)
        self.setButton = QPushButton("Set number of spills displayed")
        self.setButton.clicked.connect(self.SetWindow)
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
        layout.addWidget(self.setButton)
        layout.addWidget(self.vtxPlot)
        layout.addWidget(self.vtyPlot)
        layout.addWidget(self.vtzPlot)
        self.setLayout(layout)
        
        self.reader = None

        if not (os.path.exists("EventVertexData")):
            path = os.path.join("EventVertexData")
            os.mkdir(path)
            with open("EventVertexData/README.txt",'w') as README:
                README.write("This directory contains npz files which each contain 4 numpy arrays saved as npy files.\n")
                README.write("The 0th array contains event IDs.\n")
                README.write("The 1st, 2nd, and 3rd arrays contain X, Y, and Z vertex positions respectively.\n")
                README.write("The arrays are saved such that the Nth event ID corresponds to the Nth instance of vertex data.\n")

        self.MAX_SPILLS = 5
        self.xScatter = []
        self.yScatter = []
        self.zScatter = []
        self.currentFile = 0
        self.position = 0
        self.spillsDisplayed = 0

        self.filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.fileCount = len(self.filenames)
        self.reader = DataReader([os.path.join("Reconstructed", filename) for filename in self.filenames], "EVENT")
        while (self.currentFile < self.fileCount):
            if (self.currentFile >= self.MAX_SPILLS):
                self.vtxPlot.removeItem(self.xScatter[self.position])
                self.vtyPlot.removeItem(self.yScatter[self.position])
                self.vtzPlot.removeItem(self.zScatter[self.position])
            self.DrawSpill()
     
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.UpdateChart)
        timer.start(500)    

    def UpdateChart(self):
        self.filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.fileCount = len(self.filenames)
        if (self.fileCount > self.currentFile):
            if (self.currentFile >= self.MAX_SPILLS):
                self.vtxPlot.removeItem(self.xScatter[self.position])
                self.vtyPlot.removeItem(self.yScatter[self.position])
                self.vtzPlot.removeItem(self.zScatter[self.position])
            self.reader = DataReader([os.path.join("Reconstructed", filename) for filename in self.filenames], "EVENT")
            self.DrawSpill()


    def SetWindow(self):
        if self.txtin.text().isdigit():
            for i in range (self.spillsDisplayed):
                self.vtxPlot.removeItem(self.xScatter[i])
                self.vtyPlot.removeItem(self.yScatter[i])
                self.vtzPlot.removeItem(self.zScatter[i])
            self.xScatter = []
            self.yScatter = []
            self.zScatter = []
            self.MAX_SPILLS = int(self.txtin.text())
            self.currentFile = max(self.currentFile-self.MAX_SPILLS,0)
            self.position = 0
            self.spillsDisplayed = 0
            self.filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
            self.fileCount = len(self.filenames)
            self.reader = DataReader([os.path.join("Reconstructed", filename) for filename in self.filenames], "EVENT")
            while (self.currentFile < self.fileCount):
                self.DrawSpill()
    
    def DrawSpill(self):
        self.reader.current_index = self.currentFile
        self.reader.grab = "EVENT"
        self.eidData = self.reader.read_data()
        self.reader.grab = "XVERTEX"
        self.vtxData = self.reader.read_data()
        self.reader.grab = "YVERTEX"
        self.vtyData = self.reader.read_data()
        self.reader.grab = "ZVERTEX"
        self.vtzData = self.reader.read_data()
        if (self.spillsDisplayed < self.MAX_SPILLS):
            self.xScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,0,255,255)))
            self.yScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(255,0,0,255)))
            self.zScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,255,0,255)))
            self.spillsDisplayed += 1
        self.xScatter[self.position].setData(self.eidData,self.vtxData)
        self.vtxPlot.addItem(self.xScatter[self.position])
        self.yScatter[self.position].setData(self.eidData,self.vtyData)
        self.vtyPlot.addItem(self.yScatter[self.position])
        self.zScatter[self.position].setData(self.eidData,self.vtzData)
        self.vtzPlot.addItem(self.zScatter[self.position])
        self.reader.grab = "SPILL"
        self.sidData = self.reader.read_data()[0]
        self.spillString = str(self.sidData)
        np.savez('EventVertexData/' + self.spillString + '.npz',self.eidData,self.vtxData,self.vtyData,self.vtzData)
        self.currentFile += 1
        self.position += 1
        self.position = self.position % self.MAX_SPILLS
        layout=self.layout()