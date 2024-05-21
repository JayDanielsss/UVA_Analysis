# Native Package | os
import os

# External Packages | NumPy
import numpy as np

# External Packages | PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QApplication, QMainWindow

# External Packages | pyqtgraph
import pyqtgraph as pg

from spinquest_gui.modules.calculations.DataReader import DataReader

# Physics

### Lorentz Dot Product
from modules.physics.calculate_physics import lorentz_dot_product

class MassHist(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.hist = pg.plot()
        self.txt = QLineEdit(self)
        self.txt.setText('Enter desired spill ID')
        self.searchButton = QPushButton('View chosen spill')
        self.searchButton.clicked.connect(self.findSpill)
        self.returnButton = QPushButton('Return to most recent spill')
        self.returnButton.clicked.connect(self.leaveSpill) 
        self.hist.setLabel('bottom','Mass bins (MeV)')
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
                mass = np.zeros((len(self.eidData)))
                for i in range (len(moms)):
                    moms[i] = np.array([self.momData[0][i],self.momData[1][i],self.momData[2][i],self.momData[3][i],self.momData[4][i],self.momData[5][i]])
                    mass[i] = calcVariables(moms[i])[0]
                bins = np.arange(min(mass)-5,max(mass)+5,(max(mass)-min(mass)+10)/100)
                massOccs = np.zeros(len(bins))
                leftEdges = bins[:-1]
                rightEdges = bins[1:]
                for i in range (len(leftEdges)):
                    for j in range(len(mass)):
                        if (mass[j] > leftEdges[i] and mass[j] <= rightEdges[i]):
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
        self.txt.clear()
    
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

def calcVariables(momentum):
    """
    Description
    ------------

    Arguments
    ------------
    (mom): the px, py, pz of the positive and negative muons.
    """
    mmu = 0.10566
    mp = 0.938
    ebeam = 120.0

    p_beam = np.array([0.0, 0.0, np.sqrt(ebeam*ebeam - mp*mp), ebeam])
    p_target = np.array([0.0, 0.0, 0.0, mp])
    p_cms = p_beam + p_target
    bv_cms = np.array([p_cms[0]/p_cms[3],p_cms[1]/p_cms[3],p_cms[2]/p_cms[3]])
    s = lorentz_dot_product(p_cms, p_cms)
    mass = np.zeros((len(momentum)))
    pT = np.zeros((len(momentum)))
    x1 = np.zeros((len(momentum)))
    x2 = np.zeros((len(momentum)))
    xF = np.zeros((len(momentum)))
    costheta = np.zeros((len(momentum)))
    sintheta = np.zeros((len(momentum)))
    phi = np.zeros((len(momentum)))

    # E of the positive muon
    energy_of_positive_muon = np.sqrt(momentum[0]*momentum[0] + momentum[1]*momentum[1] + momentum[2]*momentum[2] + mmu*mmu)

    # E of the negative muon
    energy_of_negative_muon = np.sqrt(momentum[3]*momentum[3] + momentum[4]*momentum[4] + momentum[5]*momentum[5] + mmu*mmu)

    # P_{mu} of the positive muon
    four_momentum_of_positive_muon = np.array([momentum[0], momentum[1], momentum[2], energy_of_positive_muon])

    # P_{mu} of the negative muon
    four_momentum_of_negative_muon = np.array([momentum[0], momentum[1], momentum[2], energy_of_negative_muon])

    # This is just total the four momentum of the two muons -- used for reconstruction
    four_momentum_total_reconstructed = four_momentum_of_positive_muon + four_momentum_of_negative_muon

    # We find the invariant mass of the di muons - multiply by -1 to make it work:
    mass = np.sqrt(-1. * lorentz_dot_product(four_momentum_total_reconstructed, four_momentum_total_reconstructed))

    # Calculate the transverse momentum:
    pT = np.sqrt(four_momentum_total_reconstructed[0]**2 + four_momentum_total_reconstructed[1]**2)

    # Calculate some Bjorken momentum fraction
    x1 = lorentz_dot_product(p_target, four_momentum_total_reconstructed) / lorentz_dot_product(p_target, p_cms)

    # Calculate some Bjorken momentum fraction
    x2 = lorentz_dot_product(p_beam, four_momentum_total_reconstructed) / lorentz_dot_product(p_beam, p_cms)
    
    # Calulate the cosine of the stupid process:
    costheta = 2.0 * (four_momentum_of_negative_muon[3]*four_momentum_of_positive_muon[2]-four_momentum_of_positive_muon[3]*four_momentum_of_negative_muon[2])/mass/ np.sqrt(mass * mass + pT * pT)
    
    # Calculate the sine of the thing:
    sintheta = np.sqrt(1 - costheta**2)

    # Azimuthal lab angle:
    phi  = np.arctan2(2.0 * np.sqrt(mass * mass + pT * pT) * (four_momentum_of_negative_muon[0]*four_momentum_of_positive_muon[1] - four_momentum_of_positive_muon[0]*four_momentum_of_negative_muon[1]),
                        mass * (four_momentum_of_positive_muon[0]*four_momentum_of_positive_muon[0] - four_momentum_of_negative_muon[0]*four_momentum_of_negative_muon[0] + four_momentum_of_positive_muon[1]*four_momentum_of_positive_muon[1] - four_momentum_of_negative_muon[1]*four_momentum_of_negative_muon[1]))
    
    # Boost reconstructed p momentum to the some frame:
    four_momentum_total_reconstructed = boost(four_momentum_total_reconstructed,-bv_cms)
    
    # One more final momentum fraction:
    xF = 2.0 * four_momentum_total_reconstructed[2] / np.sqrt(s) / (1.0 - mass * mass / s)

    print(f"> Mass was calcualted to be: {mass}")

    return mass, pT, x1, x2, xF, costheta, sintheta, phi