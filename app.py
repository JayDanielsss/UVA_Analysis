import sys
import os
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem,QLabel,QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QGridLayout
import pyqtgraph as pg
import numpy as np
from DataReader import DataReader
from hitDisplay import HitDisplay

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from SpillCharts import SpillCharts
from StripCharts import StripCharts
from VertexHists import VertHists


from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# class OccPlotter(QWidget):
#     def __init__(self,DC,Hodo,Prop):
#         super().__init__()

#         layout = QHBoxLayout()
#         self.setLayout(layout)

#         # Create a PlotWidget to display the hit matrix
#         self.plot_widget = pg.PlotWidget()
#         layout.addWidget(self.plot_widget,stretch = 2)
       
#         self.plot_Occ(DC,Title="Drift Chamber Occ")
#         self.plot_widget = pg.PlotWidget()
#         layout.addWidget(self.plot_widget,stretch = 2)

#         self.plot_Occ(Hodo,Title="Hodo Occ")

#         self.plot_widget = pg.PlotWidget()
#         layout.addWidget(self.plot_widget,stretch = 2)
#         self.plot_Occ(Prop,Title="Prop Occ")

#         layout.addWidget(VertHists(),stretch = 8)


#     def plot_Occ(self,Occ,Title):
#         y,x = np.histogram(Occ.flatten(), bins=20)
#         hist = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
#         self.plot_widget.setTitle(Title)
#         self.plot_widget.addItem(hist)


        
        

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
        
        geometery = np.loadtxt("geometery.csv", delimiter=",", dtype=str)
        
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
        self.setData()

    def setData(self):

        #Direct Data
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MetaDATA")
        self.plot_data = self.data_reader.read_data()

        # #Momentum
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MOMENTUM")
        self.plot_data = self.data_reader.read_data()
        meanPX = np.mean(self.plot_data[0])
        meanPY = np.mean(self.plot_data[1])
        meanPZ = np.mean(self.plot_data[2])

        del(self.plot_data)

        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MetaDATA")
        self.plot_data = self.data_reader.read_data()
        RunID = self.plot_data[0][0]
        SpillID = self.plot_data[1][0]

        data = [
            ("Run ID", RunID),
            ("Spill ID",  SpillID),
            ("Total Hits",  0),
            ("PX",meanPX),
            ("PY",meanPY),
            ("PZ",meanPZ)

            
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


class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        #layout = QGridLayout()
        layout = QVBoxLayout()  # Create one QVBoxLayout
        self.setLayout(layout)


        self.data_reader = None
        self.plot_data = None
        self.previous_plot_data = None

        self.currentFile = 0


        
        
        # self.momentumPlot = StaticHistogram(self.plot_data)
        # layout.addWidget(self.momentumPlot)

        
        #Hitmatrix Plot
        self.draw_hitmatrix()

        # Add update button
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_plots)
        layout.addWidget(self.update_button)

        #timer = QTimer(self)
        #timer.timeout.connect(self.update_plots)
        #timer.start(500)   

    def update_plots(self):
        layout = self.layout()
        self.deleteItemsOfLayout(self.hit_layout)
        #layout.removeItem(self.hit_layout)
        self.draw_hitmatrix()
       

    def draw_hitmatrix(self):
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"HIT")
        self.data_reader.current_index = self.currentFile
        self.currentFile += 1
        self.plot_data = self.data_reader.read_data()
        self.hits = self.plot_data[1]
    
        num_events = 20 #len(hits)
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
        self.hit_layout.addWidget(Readout, stretch=3)

        layout = self.layout()
        layout.addLayout(self.hit_layout)

    def deleteItemsOfLayout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)



class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        vertexStrip_layout = QVBoxLayout()
        vertexStrip_layout.addWidget(SpillCharts())
        vertexStrip_layout.addWidget(StripCharts())


        layout.addLayout(vertexStrip_layout,stretch = 4) 



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

class App(QMainWindow):
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
        tab1 = Tab1()
        tab2 = Tab2()
        #tab3 = SpillCharts()

        tabs.addTab(tab1, "Main Display")
        
       # tabs.addTab(tab3, "Spill")
        self.setCentralWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()

    window2 = StripChartWindow()
    window2.show()
    sys.exit(app.exec_())
