# Native Package | os
import os

# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QTimer

# Something | DataReader
from DataReader import DataReader

# Something | HitDisplay
from hitDisplay import HitDisplay

class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        #layout = QGridLayout()
        layout = QVBoxLayout()  # Create one QVBoxLayout
        self.txtBox = QLineEdit(self)
        self.viewButton = QPushButton("View input Spill number\n")
        self.viewButton.clicked.connect(self.viewSpill)
        layout.addWidget(self.txtBox)
        layout.addWidget(self.viewButton)
        self.setLayout(layout)


        self.data_reader = None
        self.plot_data = None
        self.previous_plot_data = None

        self.file = 0
        self.hit_layout_exists = False

        # self.momentumPlot = StaticHistogram(self.plot_data)
        # layout.addWidget(self.momentumPlot)

        #Hitmatrix Plot
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.fileNo = len(filenames)
        if (self.fileNo > 0):
            self.file = self.fileNo-1
            self.draw_hitmatrix()

        # Add update button
        #self.update_button = QPushButton("Update")
        #self.update_button.clicked.connect(self.update_plots)
        #layout.addWidget(self.update_button)

        timer = QTimer(self)
        timer.timeout.connect(self.update_plots)
        timer.start(3000)
        #timer has to be long because the loading takes a while (if only we did this in c++ or i was better at optimizing python)
               

    def update_plots(self):
        layout = self.layout()
        #if (self.currentFile < self.fileCount):
         #   self.deleteItemsOfLayout(self.hit_layout)
        self.draw_hitmatrix()
       

    def draw_hitmatrix(self):
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.fileNo = len(filenames)
        if (self.file < self.fileNo):
            if (self.hit_layout_exists):
                self.deleteItemsOfLayout(self.hit_layout)
            self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"HIT")
            self.data_reader.current_index = self.file
            self.plot_data = self.data_reader.read_data()
            self.hits = self.plot_data[1]
    
            num_events = len(self.hits)
            hitmatrix = np.zeros((num_events,1000,2))

            DriftChamber = np.zeros((num_events,24))
            Hodoscope = np.zeros((num_events,15))
            propTube = np.zeros((num_events,7))

            for i in range(num_events):
                hitM, DC, Hodo, Prop = HitDisplay.getOcc(self,self.hits, event=i)
                padded_hitM = np.zeros((1000, 2))
                padded_hitM[:hitM.shape[0], :] = hitM
                hitmatrix[i] = padded_hitM
            
                #occupancy
                DriftChamber[i] = DC
                Hodoscope[i] = Hodo
                propTube[i] = Prop

            del(self.hits)
            #Hitmatrix Display
            self.hit_layout = QHBoxLayout()
            self.hit_layout_exists = True

            x_range = (29, 33)
            y_range = (0, 23)
        #Hodo1
            self.hit_matrix_plotter = HitMatrixPlotter(hitmatrix,Station=Hodoscope[:,:4],Plane=np.arange(6,10),x_range=x_range, y_range=y_range,Title="Hodo: 1")
            self.hit_layout.addWidget(self.hit_matrix_plotter,stretch=3)

        

            x_range = (0, 6)
            y_range = (0, 201)
            #DC1
            self.hit_matrix_plotter2 = HitMatrixPlotter(hitmatrix,Station=DriftChamber[:,:6],Plane=np.arange(0,6),x_range=x_range, y_range=y_range,Title="DC St: 1")
            self.hit_layout.addWidget(self.hit_matrix_plotter2,stretch=3)

            x_range = (12, 17)
            y_range = (0, 128)
            #DC2
            self.hit_matrix_plotter3 = HitMatrixPlotter(hitmatrix,Station=DriftChamber[:,6:12],Plane=np.arange(20,26),x_range=x_range, y_range=y_range,Title="DC St: 2")
            self.hit_layout.addWidget(self.hit_matrix_plotter3,stretch=3)

            x_range = (33, 37)
            y_range = (0, 19)
            #Hodo2
            self.hit_matrix_plotter4 = HitMatrixPlotter(hitmatrix,Station=Hodoscope[:,4:8],Plane=np.arange(26,30),x_range=x_range, y_range=y_range,Title="Hodo: 2")
            self.hit_layout.addWidget(self.hit_matrix_plotter4,stretch=3)

            x_range = (17, 23)
            y_range = (0, 134)
            #DC3M
            self.hit_matrix_plotter5 = HitMatrixPlotter(hitmatrix,Station=DriftChamber[:,12:18],Plane=np.arange(34,40),x_range=x_range, y_range=y_range,Title="DC St:3m")
            self.hit_layout.addWidget(self.hit_matrix_plotter5,stretch=3)

            x_range = (23, 29)
            y_range = (0, 134)
            #DC3P
            self.hit_matrix_plotter6 = HitMatrixPlotter(hitmatrix,Station=DriftChamber[:,18:24],Plane=np.arange(40,46),x_range=x_range, y_range=y_range,Title="DC St:3p")
            self.hit_layout.addWidget(self.hit_matrix_plotter6,stretch=3)

            x_range = (37, 45)
            y_range = (0, 16)
            #Hodo 3 & 4
            self.hit_matrix_plotter7 = HitMatrixPlotter(hitmatrix,Station=Hodoscope[:,8:20],Plane=[46,47,66,67,86,87,88,89],x_range=x_range, y_range=y_range,Title="Hodo: 3 & 4")
            self.hit_layout.addWidget(self.hit_matrix_plotter7,stretch=3)

            x_range = (45, 54)
            y_range = (0, 72)

            #Prop
            self.hit_matrix_plotter8 = HitMatrixPlotter(hitmatrix,Station=propTube,Plane=[8,8,8,8,8,8,8,8,8],x_range=x_range, y_range=y_range,Title="Prop Tubes")
            self.hit_layout.addWidget(self.hit_matrix_plotter8,stretch=3) 
        
            Readout = MyTable(6,2)
            Readout.setData(self.file)
            self.hit_layout.addWidget(Readout, stretch=3)

            layout = self.layout()
            layout.addLayout(self.hit_layout)
            self.file += 1

    def deleteItemsOfLayout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

    def viewSpill(self):
        spillString = self.txtBox.text()
        if (spillString.isdigit()):
            spill = int(spillString)
            self.file = 0
            filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
            self.fileNo = len(filenames)
            self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"SPILL")
            for i in range (self.fileNo):
                self.data_reader.current_index = self.file
                sidData = self.data_reader.read_data()[0]
                if (spill == sidData):
                    self.draw_hitmatrix()
                    break
                elif (self.file < self.fileNo-1):
                    self.file += 1
                else:
                    print("Spill not found!\n")