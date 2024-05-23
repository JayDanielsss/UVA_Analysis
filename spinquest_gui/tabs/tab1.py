# Native Package | os
import os

# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg

# Something | DataReader
from spinquest_gui.modules.calculations.DataReader import DataReader

# Something | HitDisplay
from spinquest_gui.plots.hitDisplay import HitDisplay

# Something | HitMatrixPlotter
from spinquest_gui.plots.HitMatrixPlotter import HitMatrixPlotter

# Something | MyTable
from spinquest_gui.plots.MyTable import MyTable

# Modules | Directories
#Should delete this?
from spinquest_gui.modules.directories.directory_health import get_reconstructed_directory

class Tab1(QWidget):

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)  # Initialize the layout with the widget as parent
        self.plot_widget = pg.PlotWidget()  # Create the plot widget
        layout.addWidget(self.plot_widget)  # Add the plot widget to the layout

        # Create QLabel for readout
        self.readout_label = QLabel(alignment=Qt.AlignLeft)
        layout.addWidget(self.readout_label)

    #     #layout = QGridLayout()
    #     self.layout = QVBoxLayout()  # Create one QVBoxLayout
    #     self.txtBox = QLineEdit(self)
    #     self.viewButton = QPushButton("View input Spill number\n")
    #    # self.viewButton.clicked.connect(self.viewSpill)
    #     self.layout.addWidget(self.txtBox)
    #     self.layout.addWidget(self.viewButton)
    #     self.setLayout(self.layout)

        # #might be outdated
        # self.data_reader = None
        # self.plot_data = None
        # self.previous_plot_data = None

        # self.file = 0
        # self.hit_layout_exists = False

        # # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # self.momentumPlot = StaticHistogram(self.plot_data)
        # layout.addWidget(self.momentumPlot)

    #     #Hitmatrix Plot
    #     filenames = sorted([filename for filename in self.reconstructed_folder_contents if filename.endswith(".npz")])
    #     self.fileNo = len(filenames)

    #     if (self.fileNo > 0):
    #         self.file = self.fileNo-1
    #         print(f"SELF FILE IS: {self.file}")
    #         self.draw_hitmatrix()

    #     # Add update button
    #     #self.update_button = QPushButton("Update")
    #     #self.update_button.clicked.connect(self.update_plots)
    #     #layout.addWidget(self.update_button)

    #     timer = QTimer(self)
    #     timer.timeout.connect(self.update_plots)
    #     timer.start(3000)
    #     #timer has to be long because the loading takes a while (if only we did this in c++ or i was better at optimizing python)
               

    # def update_plots(self):
    #     layout = self.layout()
    #     #if (self.currentFile < self.fileCount):
    #      #   self.deleteItemsOfLayout(self.hit_layout)
    #     self.draw_hitmatrix()
       

    def draw_hitmatrix(self):


        ith_event = 0
        elementid, detectorid, selectedEvents, sid, hits, eventID, track= self.organizer.grab_HitInfo()
        hitmatrices = HitDisplay()
        scatter_raw = hitmatrices.Raw_Hit(elementid,detectorid, selectedEvents, sid, eventID, ith_event)
        scatter_cluster = hitmatrices.Cluster_Hit(hits,selectedEvents,sid,eventID, ith_event)
        scatter_mup, scatter_mum = hitmatrices.Track_Hits(selectedEvents,sid,eventID,track, ith_event)
        
        # Clear the plot widget before drawing new data
        self.plot_widget.clear()
        # Add the scatter plot items to the plot widget
        self.plot_widget.addItem(scatter_raw)
        self.plot_widget.addItem(scatter_cluster)
        self.plot_widget.addItem(scatter_mup)
        self.plot_widget.addItem(scatter_mum)

        #Get Occupancy 
        DC, Hodo, propTube = hitmatrices.getOcc(hits,selectedEvents, eventID,ith_event)

        #get precentage per spill
        nelem_DC = np.array([201,201,160,160,201,201,384,384,320,320,384,384,128,128,112,112
                          ,128,	128,134,134,116,116,134,134,134,134,116,116,134,134])
  
        nelem_hodo = np.array([20,20,23,23,	19,	19,	16,	16,	16,16,16,	16,16,	16,	16,	16,])
        nelem_prop = 8

        
        DC_Percentage = (DC/nelem_DC)*100
        Avg_DC_Occ = np.average(DC_Percentage)
        Total_DC = np.sum(DC)
        hodo_Percentage = (Hodo/nelem_hodo)*100
        Avg_hodo_Occ = np.average(hodo_Percentage)
        Total_hodo = np.sum(Hodo)
        prop_Percentage = (propTube/nelem_prop)*100
        Avg_prop_Occ = np.average(prop_Percentage)
        Total_prop = np.sum(propTube)

        total_avg_per_spill = Avg_DC_Occ+Avg_hodo_Occ+Avg_prop_Occ
        total_occ_per_spill = Total_DC+Total_hodo+Total_prop

        text = f"Occupancy\nAvg Hits per Event: {total_avg_per_spill:.0f}%\nTotal Hits per Spill: {total_occ_per_spill}\n"
        self.readout_label.setText(text)

    #need to fix table!
    # def readout_table(self):
    #     self.sid, self.rid = self.organizer.grab_meta()
    #     self.mom = self.organizer.grab_mom() 

    #     MyTable.setData(self.mom,self.rid,self.sid,2,2)



        
        
        

        
    def tab(self,organizer):
        # Call the organizeData() method to populate the necessary attributes
        self.organizer = organizer
        self.organizer.organizeData()
        self.draw_hitmatrix()
       # self.readout_table()





    # def deleteItemsOfLayout(self,layout):
    #     if layout is not None:
    #         while layout.count():
    #             item = layout.takeAt(0)
    #             widget = item.widget()
    #             if widget is not None:
    #                 widget.setParent(None)

    # def viewSpill(self):
    #     spillString = self.txtBox.text()
    #     if (spillString.isdigit()):
    #         spill = int(spillString)
    #         self.file = 0
    #         filenames = sorted([filename for filename in self.reconstructed_folder_contents if filename.endswith(".npz")])
    #         self.fileNo = len(filenames)
    #         self.data_reader = DataReader([os.path.join(get_reconstructed_directory(), filename) for filename in filenames],"SPILL")
    #         for i in range (self.fileNo):
    #             self.data_reader.current_index = self.file
    #             sidData = self.data_reader.read_data()[0]
    #             if (spill == sidData):
    #                 self.draw_hitmatrix()
    #                 break
    #             elif (self.file < self.fileNo-1):
    #                 self.file += 1
    #             else:
    #                 print("Spill not found!\n")