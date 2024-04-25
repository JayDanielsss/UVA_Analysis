import sys
import os
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
from random import randrange, uniform
from PyQt5 import QtTest
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from DataReader import DataReader
import pyqtgraph as pg

class SpillCharts(QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout()
        self.vtxPlot=pg.plot()
        self.vtyPlot=pg.plot()
        self.vtzPlot=pg.plot()
        self.vtxPlot.showGrid(x=True,y=True)
        self.vtxPlot.setLabel('bottom',"Spill ID")
        self.vtxPlot.setLabel('left',"X Vertex (cm)")
        self.vtyPlot.showGrid(x=True,y=True)
        self.vtyPlot.setLabel('bottom',"Spill ID")
        self.vtyPlot.setLabel('left',"Y Vertex (cm)")
        self.vtzPlot.showGrid(x=True,y=True)
        self.vtzPlot.setLabel('bottom',"Spill ID")
        self.vtzPlot.setLabel('left',"Z Vertex (cm)")
        layout.addWidget(self.vtxPlot)
        layout.addWidget(self.vtyPlot)
        layout.addWidget(self.vtzPlot)
        self.setLayout(layout)
        
        self.runButton=QPushButton("Run")
        self.runButton.setCheckable(True)
        self.runButton.setChecked(False)
        self.runButton.clicked.connect(self.UpdateChart)
        layout.addWidget(self.runButton)
        
        self.reader = None

    def UpdateChart(self):
        self.dt=1000
        if self.runButton.isChecked():
            self.vtxPlot.clear()
            self.vtyPlot.clear()
            self.vtzPlot.clear()
            currentFile = 0
        while self.runButton.isChecked():
            self.filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npy")])
            self.fileCount = len(self.filenames)
            if (self.fileCount > currentFile):
                self.reader = DataReader([os.path.join("Reconstructed", filename) for filename in self.filenames], "EVENT")
                self.reader.current_index = currentFile
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
                self.xScatter=pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,0,255,255))
                self.yScatter=pg.ScatterPlotItem(size=10,brush=pg.mkBrush(255,0,0,255))
                self.zScatter=pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,255,0,255))
                self.xErr = pg.ErrorBarItem(x=self.sidData,y=self.vtxMean,height=self.vtxSTD,pen=pg.mkPen(0,0,255,255),beam=0.5)
                self.xScatter.addPoints(self.sidData,self.vtxMean)
                self.vtxPlot.addItem(self.xScatter)
                self.vtxPlot.addItem(self.xErr)
                self.yErr = pg.ErrorBarItem(x=self.sidData,y=self.vtyMean,height=self.vtySTD,pen=pg.mkPen(255,0,0,255),beam=0.5)
                self.yScatter.addPoints(self.sidData,self.vtyMean)
                self.vtyPlot.addItem(self.yScatter)
                self.vtyPlot.addItem(self.yErr)
                self.zErr = pg.ErrorBarItem(x=self.sidData,y=self.vtzMean,height=self.vtzSTD,pen=pg.mkPen(0,255,0,255),beam=0.5)
                self.zScatter.addPoints(self.sidData,self.vtzMean)
                self.vtzPlot.addItem(self.zScatter)
                self.vtzPlot.addItem(self.zErr)
                currentFile += 1
                layout=self.layout()
            QtTest.QTest.qWait(self.dt)