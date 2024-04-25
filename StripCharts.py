#strip charts for x,y,z vertices w.r.t event id

import sys
import os
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
from random import randrange, uniform
from PyQt5 import QtTest
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from DataReader import DataReader
import pyqtgraph as pg

class StripCharts(QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout()
        self.vtxPlot=pg.plot()
        self.vtyPlot=pg.plot()
        self.vtzPlot=pg.plot()
        self.vtxPlot.showGrid(x=True,y=True)
        self.vtxPlot.setLabel('bottom',"Event ID")
        self.vtxPlot.setLabel('left',"X Vertex (cm)")
        self.vtyPlot.showGrid(x=True,y=True)
        self.vtyPlot.setLabel('bottom',"Event ID")
        self.vtyPlot.setLabel('left',"Y Vertex (cm)")
        self.vtzPlot.showGrid(x=True,y=True)
        self.vtzPlot.setLabel('bottom',"Event ID")
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
                self.eidData = self.reader.read_data()
                self.reader.grab = "XVERTEX"
                self.vtxData = self.reader.read_data()
                self.reader.grab = "YVERTEX"
                self.vtyData = self.reader.read_data()
                self.reader.grab = "ZVERTEX"
                self.vtzData = self.reader.read_data()
                self.xScatter=pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,0,255,255))
                self.yScatter=pg.ScatterPlotItem(size=10,brush=pg.mkBrush(255,0,0,255))
                self.zScatter=pg.ScatterPlotItem(size=10,brush=pg.mkBrush(0,255,0,255))
                self.xScatter.addPoints(self.eidData,self.vtxData)
                self.vtxPlot.addItem(self.xScatter)
                self.yScatter.addPoints(self.eidData,self.vtyData)
                self.vtyPlot.addItem(self.yScatter)
                self.zScatter.addPoints(self.eidData,self.vtzData)
                self.vtzPlot.addItem(self.zScatter)
                currentFile += 1
                layout=self.layout()
            QtTest.QTest.qWait(self.dt)