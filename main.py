#####################
### SpinQuest GUI ###
###  J, S, M, D   ###
#####################

# Native Package | os
import os

# Native Package | sys
import sys

# External Packages | 
from spinquest_gui.statics.constants import _APPLICATION_NAME, _WINDOW_MAIN_APP_WIDTH, _WINDOW_MAIN_APP_HEIGHT

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem,QLabel,QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLineEdit
import pyqtgraph as pg
import numpy as np
from DataReader import DataReader
from hitDisplay import HitDisplay

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from StripCharts import StripCharts
from MassHist import MassHist


from PyQt5.QtWidgets import QWidget, QVBoxLayout 

from spinquest_gui.tabs.tab1 import Tab1
from spinquest_gui.tabs.tab2 import Tab2

class HitMatrixPlotter(QWidget):
    def __init__(self, hitmatrix,Station,Plane, x_range=None, y_range=None,Title=None):
        super().__init__()

        # Create a layout to hold the plot widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a PlotWidget to display the hit matrix
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Plot the hit matrix
        self.plot_hitmatrix(hitmatrix)

        # Set custom axis ranges if provided
        if x_range is not None:
            self.plot_widget.setXRange(*x_range)
        if y_range is not None:
            self.plot_widget.setYRange(*y_range)
        if Title is not None:
            self.plot_widget.setTitle(Title)

        # Create QLabel for readout
        self.readout_label = QLabel(alignment=Qt.AlignLeft)
        layout.addWidget(self.readout_label)

        # Update readout
        # self.update_readout(70, 0.7)
        self.getStationOcc(Station,Plane)

    def plot_hitmatrix(self, hitmatrix):
        # Extract data from the hit matrix
        elemid = hitmatrix[:, :, 1].flatten()
        detid = hitmatrix[:, :, 0].flatten()

        # Create a scatter plot
        scatter_plot = pg.ScatterPlotItem()
        scatter_plot.setData(x=detid, y=elemid, pen=None, symbol='s')

        # Set labels for each axis
        self.plot_widget.setLabel('bottom', text='Det ID')
        self.plot_widget.setLabel('left', text='Elem ID')

        # Add scatter plot to the PlotWidget
        self.plot_widget.addItem(scatter_plot)

    def getStationOcc(self,detector,Plane):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, 'spinquest_gui', 'statics', 'geometry.csv')

        geometery = np.loadtxt(csv_path, delimiter = ",", dtype = str)
        
        PerEvent = np.zeros_like(detector)
        
        for i in range(len(detector)):
            for j in range(len(detector[0])):
                PerEvent[i,j] = detector[i,j]/int(geometery[Plane[j]][1])

        AvgOccPerSpill = np.average(PerEvent)
        TotalOccPerSpill = np.sum(detector)

        text = f"Occupancy\nAvg Hits per Event: {AvgOccPerSpill*100:.0f}%\nTotal Hits per Spill: {TotalOccPerSpill}\n"
        self.readout_label.setText(text)

class MyTable(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.setGeometry(0, 0, 400, 300)

        # Insert data into the table

    def setData(self,fileNumber):

        #Direct Data
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MetaDATA")
        self.data_reader.current_index = fileNumber
        self.plot_data = self.data_reader.read_data()

        # #Momentum
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MOMENTUM")
        self.data_reader.current_index = fileNumber
        self.plot_data = self.data_reader.read_data()
        meanPX = np.mean(self.plot_data[0])
        meanPY = np.mean(self.plot_data[1])
        meanPZ = np.mean(self.plot_data[2])
        totalHits = self.plot_data[3]

        del(self.plot_data)

        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MetaDATA")
        self.data_reader.current_index = fileNumber
        self.plot_data = self.data_reader.read_data()
        RunID = self.plot_data[0][0]
        SpillID = self.plot_data[1][0]

        data = [
            ("Run ID", RunID),
            ("Spill ID",  SpillID),
            ("Total Hits",  totalHits),
            ("PX",round(meanPX,4)),
            ("PY",round(meanPY,4)),
            ("PZ",round(meanPZ,4))

            
        ]


        # Populate the table with data
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(str(value))
                self.setItem(row, col, item)




    

class StaticHistogram(QWidget):
    def __init__(self,data):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.plot_widgets = []

        self.plot_data = data
        
        self.create_histograms()

    def create_histograms(self):
        for plot_data, color in zip([self.plot_data], [(0, 0, 255, 150)]):
            
            plot_layout = QHBoxLayout()
            plot_widget = pg.PlotWidget()
            hist, bins = np.histogram(plot_data[0], bins=100)
            plot_widget.plot(bins, hist, stepMode=True, fillLevel=0, brush=color)
            plot_layout.addWidget(plot_widget)
            plot_widget.setTitle("PX = {}".format(np.mean(plot_data[0])))
            self.plot_widgets.append(plot_widget)
            self.layout().addLayout(plot_layout)

         


            plot_widget2 = pg.PlotWidget()
            hist, bins = np.histogram(plot_data[1], bins=100)
            plot_widget2.plot(bins, hist, stepMode=True, fillLevel=0, brush=color)
            plot_layout.addWidget(plot_widget2)
            plot_widget2.setTitle("PY = {}".format(np.mean(plot_data[1])))
            self.plot_widgets.append(plot_widget2)
            self.layout().addLayout(plot_layout)

            plot_widget3 = pg.PlotWidget()
            hist, bins = np.histogram(plot_data[2], bins=100)
            plot_widget3.plot(bins, hist, stepMode=True, fillLevel=0, brush=color)
            plot_layout.addWidget(plot_widget3)
            plot_widget3.setTitle("PZ = {}".format(np.mean(plot_data[2])))
            self.plot_widgets.append(plot_widget3)
            self.layout().addLayout(plot_layout)



class HistogramComparisonPlot(QWidget):
    def __init__(self, vtx_data, previous_data=None):
        super().__init__()
        #layout = QHBoxLayout()
        #self.setLayout(layout)
        self.plot_widgets = []

        self.plot_data = vtx_data
        self.previous_plot_data = previous_data

        self.create_histograms()

    def create_histograms(self):
        for data, color in zip([self.plot_data, self.previous_plot_data], [(0, 0, 255, 150), (255, 0, 0, 150)]):
            #plot_layout = QVBoxLayout()
            
            plot_widget = pg.PlotWidget()
            hist, bins = np.histogram(data[:,0], bins=50)
            plot_widget.plot(bins, hist, stepMode=True, fillLevel=0, brush=color)
            #plot_layout.addWidget(plot_widget)
            self.plot_widgets.append(plot_widget)
            #self.layout().addLayout(plot_layout)

class StripChartWindow(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'SpinQuest Display'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        tabs = QTabWidget()
        tab2 = Tab2()
        tabs.addTab(tab2, "StripCharts")
        self.setCentralWidget(tabs)

# PyQT Window | Main Window
class App(QMainWindow):

    def __init__(self):

        super().__init__()

        # Set the name of the application:
        self.title = _APPLICATION_NAME
        self.setWindowTitle(self.title)

        # Configure the geometry of the application window:
        self.window_left = 0
        self.window_top = 0
        self.window_width = _WINDOW_MAIN_APP_WIDTH
        self.window_height = _WINDOW_MAIN_APP_HEIGHT
        self.setGeometry(self.window_left, self.window_top, self.window_width, self.window_height)

        # Initalize additional UI:
        self.initializeUI()

    def initializeUI(self):

        # Initialize PyQT's "central widget"
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize the central widget's tabs:
        # self.tab1 = Tab1()
        
        tab1 = Tab1()
        # tab2 = MassHist()

        self.central_widget.addTab(tab1, "Main Display")
        # self.central_widget.addTab(tab2,"Mass Histogram")
        
       # tabs.addTab(tab3, "Spill")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()

    window2 = StripChartWindow()
    window2.show()
    sys.exit(app.exec_())
