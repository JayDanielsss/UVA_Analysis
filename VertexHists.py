import sys
import os
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
from random import randrange, uniform
from PyQt5 import QtTest
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from DataReader import DataReader
import pyqtgraph as pg

class VertHists(QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout()
        self.vtxPlot=pg.plot()
        self.vtyPlot=pg.plot()
        self.vtzPlot=pg.plot()
        self.vtxPlot.showGrid(x=True,y=True)
        self.vtxPlot.setLabel('bottom',"X Vertex (cm)")
        self.vtxPlot.setLabel('left',"Occurences")
        self.vtyPlot.showGrid(x=True,y=True)
        self.vtyPlot.setLabel('bottom',"Y Vertex (cm)")
        self.vtyPlot.setLabel('left',"Occurences")
        self.vtzPlot.showGrid(x=True,y=True)
        self.vtzPlot.setLabel('bottom',"Z Vertex (cm)")
        self.vtzPlot.setLabel('left',"Occurences")
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
        binNo = 200
        if self.runButton.isChecked():
            self.vtxPlot.clear()
            orthoBinEdges = np.arange(-1.0,1.0,1.0/binNo)
            xOccurences = np.zeros(orthoBinEdges.size-1)
            self.vtyPlot.clear()
            yOccurences = np.zeros(orthoBinEdges.size-1)
            self.vtzPlot.clear()
            paraBinEdges = np.arange(-400,400,400/binNo)
            zOccurences = np.zeros(paraBinEdges.size-1)
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
                for i in range(self.vtxData.size):
                    for j in range(orthoBinEdges.size-1):
                        if orthoBinEdges[j] < self.vtxData[i] < orthoBinEdges[j+1]:
                            xOccurences[j] +=1
                            break
                self.xBar=pg.BarGraphItem(x0 = orthoBinEdges[:-1],x1= orthoBinEdges[1:],height = xOccurences, brush=pg.mkBrush(0,0,255,255))
                for i in range(self.vtyData.size):
                    for j in range(orthoBinEdges.size-1):
                        if orthoBinEdges[j] < self.vtyData[i] < orthoBinEdges[j+1]:
                            yOccurences[j] +=1
                            break
                self.yBar=pg.BarGraphItem(x0 = orthoBinEdges[:-1],x1=orthoBinEdges[1:],height = yOccurences, brush=pg.mkBrush(255,0,0,255))
                for i in range(self.vtzData.size):
                    for j in range(paraBinEdges.size-1):
                        if paraBinEdges[j] < self.vtzData[i] < paraBinEdges[j+1]:
                            zOccurences[j] +=1
                            break
                self.zBar=pg.BarGraphItem(x0 = paraBinEdges[:-1],x1=paraBinEdges[1:],height = zOccurences, brush=pg.mkBrush(0,255,0,255))
                self.vtxPlot.addItem(self.xBar)
                self.vtyPlot.addItem(self.yBar)
                self.vtzPlot.addItem(self.zBar)
                currentFile += 1
                layout=self.layout()
            QtTest.QTest.qWait(self.dt)