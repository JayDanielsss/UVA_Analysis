import os
import numpy as np
from pyqtgraph.Qt import QtGui
from random import randrange, uniform
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QApplication, QMainWindow
from DataReader import DataReader
import pyqtgraph as pg

class MassHist(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.hist = pg.plot()
        self.txt = QLineEdit(self)
        self.searchButton = QPushButton('View chosen spill')
        self.searchButton.clicked.connect(self.findSpill)
        self.returnButton = QPushButton('Return to most recent spill')
        self.returnButton.clicked.connect(self.leaveSpill) 
        self.hist.setLabel('bottom','Mass bins')
        self.hist.setLabel('left','Occurences in spill')
        layout.addWidget(self.txt)
        layout.addWidget(self.searchButton)
        layout.addWidget(self.returnButton)
        layout.addWidget(self.hist)
        self.setLayout(layout)

        if not (os.path.exists("MassData")):
            path = os.path.join("MassData")
            os.mkdir(path)
            with open("MassData/README.txt",'w') as README:
                README.write("This directory contains .npz files labeled by spill. Each file contains 2 arrays\n")
                README.write("arr_0 is the array containing event IDs and arr_1 is the array containing masses\n")
                README.write("The event ID stored in the nth index of arr_0 corresponds to the mass data stored in the nth index of arr_1\n")

        self.reader = None

        self.currentFile = 0

        self.barItemExists = False
        self.viewingOldSpill = False

        self.filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.fileCount = len(self.filenames)
        self.reader = DataReader([os.path.join("Reconstructed", filename) for filename in self.filenames], "MOMENTUM")

        if (self.fileCount > 0):
            self.currentFile = self.fileCount-1
            self.drawHist()


        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.drawHist)
        timer.start(500)    
    
    def drawHist(self):
        if not (self.viewingOldSpill):
            self.filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
            self.fileCount = len(self.filenames)
            if (self.currentFile < self.fileCount):
                if (self.barItemExists):
                    self.hist.removeItem(self.bar)
                self.reader = DataReader([os.path.join("Reconstructed", filename) for filename in self.filenames], "MOMENTUM")
                self.reader.current_index = self.currentFile
                self.momData = self.reader.read_data()
                self.reader.grab = "EVENT"
                self.eidData = self.reader.read_data()
                moms = np.zeros((len(self.eidData),6))
                mass = np.zeros((len(self.eidData),6))
                for i in range (len(moms)):
                    moms[i] = np.array([self.momData[0][i],self.momData[1][i],self.momData[2][i],self.momData[3][i],self.momData[4][i],self.momData[5][i]])
                    mass[i] = calcVariables(moms[i])[0]
                bins = np.arange(0,1,0.01)
                massOccs = np.zeros(len(bins))
                leftEdges = bins[:-1]
                rightEdges = bins[1:]
                for i in range (len(leftEdges)):
                    for j in range(len(mass)):
                        for k in range(len(mass[j])):
                            if (mass[j][k] >= leftEdges[i] and mass[j][k] <= rightEdges[i]):
                                massOccs[i] += 1
                self.bar = pg.BarGraphItem(x0=leftEdges,x1=rightEdges,height=massOccs,brush = pg.mkBrush("#ffb3cc"))
                self.hist.addItem(self.bar)
                self.barItemExists = True
                self.currentFile+=1
                self.reader.grab = "SPILL"
                self.sidData = self.reader.read_data()[0]
                spillString = str(self.sidData)
                np.savez('MassData/' + spillString + '.npz',self.eidData,mass)
                layout = self.layout()
    
    def findSpill(self):
        spillString = self.txt.text()
        if (spillString.isdigit()):
            spill = int(spillString)
            self.currentFile = 0
            filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
            self.fileCount = len(filenames)
            self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"SPILL")
            for i in range (self.fileCount):
                self.data_reader.current_index = self.currentFile
                sidData = self.data_reader.read_data()[0]
                if (spill == sidData):
                    self.viewingOldSpill = False
                    self.drawHist()
                    self.viewingOldSpill = True
                    break
                elif (self.currentFile < self.fileCount-1):
                    self.currentFile += 1
                else:
                    print("Spill not found!\n")

    def leaveSpill(self):
        self.viewingOldSpill = False
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.fileCount = len(filenames)
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"SPILL")
        if (self.fileCount > 0):
            self.currentFile = self.fileCount-1
        self.drawHist()
        






def lorentz_dot(a, b):
    metric = np.array([-1, -1, -1, 1])  # Lorentzian metric signature (+, -, -, -)
    return np.dot(a*metric, b)

def boost(vector, boost_v):
    bx, by, bz = boost_v[0], boost_v[1], boost_v[2]
    b2 = bx**2 + by**2 + bz**2
    ggamma = 1.0 / np.sqrt(1.0 - b2)
    bp = bx * vector[0] + by * vector[1] + bz * vector[2]
    gamma2 = (ggamma - 1.0) / b2

    vector[0] += gamma2 * bp * bx + ggamma * bx * vector[3]
    vector[1] += gamma2 * bp * by + ggamma * by * vector[3]
    vector[2] += gamma2 * bp * bz + ggamma * bz * vector[3]
    vector[3] = ggamma * (vector[3] + bp)
   
    return vector

def calcVariables(mom):
    mmu=0.10566
    mp = 0.938
    ebeam = 120.0
    p_beam = np.array([0.0, 0.0, np.sqrt(ebeam*ebeam - mp*mp), ebeam])
    p_target = np.array([0.0, 0.0, 0.0, mp])
    p_cms = p_beam + p_target
    bv_cms = np.array([p_cms[0]/p_cms[3],p_cms[1]/p_cms[3],p_cms[2]/p_cms[3]])
    s = lorentz_dot(p_cms, p_cms)
    mass=np.zeros((len(mom)))
    pT=np.zeros((len(mom)))
    x1=np.zeros((len(mom)))
    x2=np.zeros((len(mom)))
    xF=np.zeros((len(mom)))
    momentum = np.zeros((len(mom)))
    costheta=np.zeros((len(mom)))
    sintheta=np.zeros((len(mom)))
    phi=np.zeros((len(mom)))
    for i in range(len(mom)):
        momentum[i] = mom[i]
        E_pos=np.sqrt(momentum[0]*momentum[0] + momentum[1]*momentum[1] + momentum[2]*momentum[2] + mmu*mmu);
        p_pos=np.array([momentum[0],momentum[1],momentum[2],E_pos])
        E_neg=np.sqrt(momentum[3]*momentum[3] + momentum[4]*momentum[4] + momentum[5]*momentum[5] + mmu*mmu);
        p_neg=np.array([momentum[3],momentum[4],momentum[5],E_neg])

        p_sum = p_pos + p_neg

        mass[i] = np.sqrt(lorentz_dot(p_sum, p_sum))
        pT[i] = np.sqrt(p_sum[0]**2+p_sum[1]**2)

        x1[i] = lorentz_dot(p_target, p_sum) / lorentz_dot(p_target, p_cms)
        x2[i] = lorentz_dot(p_beam, p_sum) / lorentz_dot(p_beam, p_cms)
       
        costheta[i] = 2.0 * (p_neg[3]*p_pos[2]-p_pos[3]*p_neg[2])/mass[i]/ np.sqrt(mass[i] * mass[i] + pT[i] * pT[i])
       
        phi[i] = np.arctan2(2.0 * np.sqrt(mass[i] * mass[i] + pT[i] * pT[i]) * (p_neg[0]*p_pos[1] - p_pos[0]*p_neg[1]),
                         mass[i]*(p_pos[0]*p_pos[0] - p_neg[0]*p_neg[0] + p_pos[1]*p_pos[1] - p_neg[1]*p_neg[1]))
        sintheta[i]=np.sqrt(1-costheta[i]**2)
        p_sum = boost(p_sum,-bv_cms)
        xF[i] = 2.0 * p_sum[2] / np.sqrt(s) / (1.0 - mass[i] * mass[i] / s)
    return mass, pT, x1, x2, xF, costheta, sintheta, phi