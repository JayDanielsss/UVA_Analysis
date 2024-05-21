import sys
import os
import numpy as np
from pyqtgraph.Qt import QtGui
from random import randrange, uniform
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QApplication
from spinquest_gui.modules.calculations.DataReader import DataReader
from types import NoneType
import pyqtgraph as pg
application = QApplication(sys.argv)

class SpillCharts(QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout()
        self.vtxSPlot=pg.plot()
        self.vtySPlot=pg.plot()
        self.vtzSPlot=pg.plot()
        self.txtin = QLineEdit(self)
        self.setButton = QPushButton("Set number of spills displayed")
        self.setButton.clicked.connect(self.SetSpillWindow)
        self.vtxSPlot.showGrid(x=True,y=True)
        self.vtxSPlot.setLabel('bottom',"Spill ID")
        self.vtxSPlot.setLabel('left',"X Vertex (cm)")
        self.vtySPlot.showGrid(x=True,y=True)
        self.vtySPlot.setLabel('bottom',"Spill ID")
        self.vtySPlot.setLabel('left',"Y Vertex (cm)")
        self.vtzSPlot.showGrid(x=True,y=True)
        self.vtzSPlot.setLabel('bottom',"Spill ID")
        self.vtzSPlot.setLabel('left',"Z Vertex (cm)")
        layout.addWidget(self.txtin)
        layout.addWidget(self.setButton)
        layout.addWidget(self.vtxSPlot)
        layout.addWidget(self.vtySPlot)
        layout.addWidget(self.vtzSPlot)
        self.setLayout(layout)
        
        self.reader = None

        self.MAX_SPILLS = 5
        self.xSScatter = []
        self.ySScatter = []
        self.zSScatter = []
        self.xErr = []
        self.yErr = []
        self.zErr = []
        self.currentFile = 0
        self.position = 0
        self.spillsDisplayed = 0

        if not (os.path.exists("SpillVertexMeans")):
            path = os.path.join("SpillVertexMeans")
            os.mkdir(path)
            with open ("SpillVertexMeans/README.txt",'w') as README:
                README.write("This directory contains npz files labeled by spill. Each file contains 7 0-dimensional arrays stored in npy files\n")
                README.write("The 0th array contains the spill ID\n")
                README.write("The 1st, 2nd, and 3rd arrays contain the mean X, Y, and Z vertex positions over all events in the spill respectively\n")
                README.write("The 4th, 5th, and 6th arrays contain the standard deviations of X, Y, and Z vertex positions respectively\n")


        self.filenames = sorted([filename for filename in os.listdir("reconstructed") if filename.endswith(".npz")])
        self.fileCount = len(self.filenames)
        while (self.fileCount > self.currentFile):
            if (self.currentFile >= self.MAX_SPILLS):
                self.vtxSPlot.removeItem(self.xSScatter[self.position])
                self.vtySPlot.removeItem(self.ySScatter[self.position])
                self.vtzSPlot.removeItem(self.zSScatter[self.position])
                self.vtxSPlot.removeItem(self.xErr[self.position])
                self.vtySPlot.removeItem(self.yErr[self.position])
                self.vtzSPlot.removeItem(self.zErr[self.position])
            self.reader = DataReader([os.path.join("reconstructed", filename) for filename in self.filenames], "EVENT")
            self.DrawSpill()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.UpdateChart)
        timer.start(500)

    def UpdateChart(self):
        self.filenames = sorted([filename for filename in os.listdir("reconstructed") if filename.endswith(".npz")])
        self.fileCount = len(self.filenames)
        if (self.fileCount > self.currentFile):
            if (self.currentFile >= self.MAX_SPILLS):
                self.vtxSPlot.removeItem(self.xSScatter[self.position])
                self.vtySPlot.removeItem(self.ySScatter[self.position])
                self.vtzSPlot.removeItem(self.zSScatter[self.position])
                self.vtxSPlot.removeItem(self.xErr[self.position])
                self.vtySPlot.removeItem(self.yErr[self.position])
                self.vtzSPlot.removeItem(self.zErr[self.position])
            self.reader = DataReader([os.path.join("reconstructed", filename) for filename in self.filenames], "EVENT")
            self.DrawSpill()

    def SetSpillWindow(self):
        if self.txtin.text().isdigit():
            for i in range (self.spillsDisplayed):
                self.vtxSPlot.removeItem(self.xSScatter[i])
                self.vtySPlot.removeItem(self.ySScatter[i])
                self.vtzSPlot.removeItem(self.zSScatter[i])
                self.vtxSPlot.removeItem(self.xErr[i])
                self.vtySPlot.removeItem(self.yErr[i])
                self.vtzSPlot.removeItem(self.zErr[i])
            self.xSScatter = []
            self.ySScatter = []
            self.zSScatter = []
            self.xErr = []
            self.yErr = []
            self.zErr = []
            self.MAX_SPILLS = int(self.txtin.text())
            self.currentFile = max(self.currentFile-self.MAX_SPILLS,0)
            self.position = 0
            self.spillsDisplayed = 0
            self.filenames = sorted([filename for filename in os.listdir("reconstructed") if filename.endswith(".npz")])
            self.fileCount = len(self.filenames)
            self.reader = DataReader([os.path.join("reconstructed", filename) for filename in self.filenames], "EVENT")
            while (self.fileCount > self.currentFile):
                self.DrawSpill()

    def DrawSpill(self):
        self.reader.current_index = self.currentFile
        self.reader.grab = "EVENT"
        self.eidData = np.array(self.reader.read_data())
        self.reader.grab = "XVERTEX"
        self.vtxData = np.array(self.reader.read_data())
        self.reader.grab = "YVERTEX"
        self.vtyData = np.array(self.reader.read_data())
        self.reader.grab = "ZVERTEX"
        self.vtzData = np.array(self.reader.read_data())
        self.reader.grab = "SPILL"
        self.sidData = np.array(self.reader.read_data()[0])
        self.vtxMean = np.array([np.mean(self.vtxData)])
        self.vtyMean = np.array([np.mean(self.vtyData)])
        self.vtzMean = np.array([np.mean(self.vtzData)])
        self.vtxSTD = np.std(self.vtxData)
        self.vtySTD = np.std(self.vtyData)
        self.vtzSTD = np.std(self.vtzData)
        if (self.spillsDisplayed < self.MAX_SPILLS):
            self.xSScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,0,255,255)))
            self.ySScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(255,0,0,255)))
            self.zSScatter.append(pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,255,0,255)))
            self.xErr.append(pg.ErrorBarItem(x=self.sidData,y=self.vtxMean,height=self.vtxSTD,pen=pg.mkPen(0,0,255,255),beam=0.5))
            self.yErr.append(pg.ErrorBarItem(x=self.sidData,y=self.vtyMean,height=self.vtySTD,pen=pg.mkPen(255,0,0,255),beam=0.5))
            self.zErr.append(pg.ErrorBarItem(x=self.sidData,y=self.vtzMean,height=self.vtzSTD,pen=pg.mkPen(0,255,0,255),beam=0.5))
            self.spillsDisplayed += 1
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
        np.savez('SpillVertexMeans/' + self.spillString + '.npz',self.sidData,self.vtxMean,self.vtyMean,self.vtzMean,self.vtxSTD,self.vtySTD,self.vtzSTD)
        self.currentFile += 1
        self.position += 1
        self.position = self.position % self.MAX_SPILLS
        layout=self.layout()