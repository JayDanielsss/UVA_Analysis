# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import pyqtgraph as pg

# Modules | HitDisplay
from app.modules.HitDisplay import HitDisplay
from app.modules.DataOrganizer import DataOrganizer

# Modules | MyTable
# from app.modules.MyTable import MyTable

class Tab1(QWidget):

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)  # Initialize the layout with the widget as parent
        self.plot_widget = pg.PlotWidget()  # Create the plot widget
        layout.addWidget(self.plot_widget)  # Add the plot widget to the layout

        # Create QLabel for readout
        self.readout_label = QLabel(alignment = Qt.AlignLeft)
        layout.addWidget(self.readout_label)

        # # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias = True)

        
        #Create an instance of dataOrganizer
        self.organizer = DataOrganizer()
        self.organizer.organizeData()
        #call tab displays
        self.tab()



    def draw_hitmatrix(self):

        ith_event = 0
        elementid, detectorid, selectedEvents, sid, hits, eventID, track= self.organizer.grab_HitInfo()
        hitmatrices = HitDisplay()
        scatter_raw = hitmatrices.Raw_Hit(elementid,detectorid, selectedEvents, sid, eventID, ith_event)
        scatter_cluster = hitmatrices.Cluster_Hit(hits,selectedEvents,sid,eventID, ith_event)
        scatter_mup, scatter_mum = hitmatrices.Track_Hits(selectedEvents,sid,eventID,track, ith_event)
        #  #Create an instance of dataOrganizer
        organizer = DataOrganizer()
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

    def tab(self):
        
        self.draw_hitmatrix()
       # self.readout_table()