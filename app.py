import sys
import os
from PyQt5.QtWidgets import QMainWindow, QLabel,QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QGridLayout
import pyqtgraph as pg
import numpy as np
from DataReader import DataReader
from hitDisplay import HitDisplay

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

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


class HitMatrixPlotter:
    def __init__(self, hitmatrix):
        super().__init__()
        self.figure = Figure(figsize=(2, 3))
        self.canvas = FigureCanvas(self.figure)
        # Dictionary to store subplot references
        subplots = {}

        # Add subplots in a 1x12 grid
        for i in range(1, 11):
            self.ax = self.figure.add_subplot(1, 10, i)
            subplots[f'ax{i}'] = self.ax  # Store subplot reference in the dictionary

        # for i in range(1, 11):
        #     self.ax = self.figure.add_subplot(2, 10, i)
        #     subplots[f'ax{i+10}'] = self.ax  # Store subplot reference in the dictionary


        # self.ax1.clear()
        # self.ax2.clear()
        elemid = hitmatrix[:,:,1]
        detid = hitmatrix[:,:,0]
        # #self.ax1.imshow(event[:32, :], cmap='binary', aspect='auto')
        subplots['ax1'].scatter(detid,elemid, marker=',')
        subplots['ax1'].set_xlim(29.5,33.5)
        subplots['ax1'].set_ylim(0,23.5)
        subplots['ax1'].set_title("Hodo: 1")

        subplots['ax2'].scatter(detid,elemid,marker=',')
        subplots['ax2'].set_xlim(-.5,6.5)
        subplots['ax2'].set_ylim(0,201.5)
        subplots['ax2'].set_title("DC: ST1")

        subplots['ax3'].scatter(detid,elemid,marker=',')
        subplots['ax3'].set_xlim(11.5,17.5)
        subplots['ax3'].set_ylim(0,128.5)
        subplots['ax3'].set_title("DC: ST2")

        subplots['ax4'].scatter(detid,elemid,marker=',')
        subplots['ax4'].set_xlim(33.5,37.5)
        subplots['ax4'].set_ylim(0,19.5)
        subplots['ax4'].set_title("Hodo: 2")

        subplots['ax5'].scatter(detid,elemid,marker=',')
        subplots['ax5'].set_xlim(17.5,23.5)
        subplots['ax5'].set_ylim(0,134.5)
        subplots['ax5'].set_title("DC: ST3M")

        subplots['ax6'].scatter(detid,elemid,marker=',')
        subplots['ax6'].set_xlim(23.5,29.5)
        subplots['ax6'].set_ylim(0,134.5)
        subplots['ax6'].set_title("DC: ST3P")

        subplots['ax7'].scatter(detid,elemid,marker=',')
        subplots['ax7'].set_xlim(37.5,39.5)
        subplots['ax7'].set_ylim(0,16.5)
        subplots['ax7'].set_title("Hodo: 3")

        subplots['ax8'].scatter(elemid,detid,marker=',')
        subplots['ax8'].set_xlim(45.5,79.5)
        subplots['ax8'].set_ylim(-1,8.5)
        subplots['ax8'].set_title("Prop Tube 1")

        subplots['ax9'].scatter(detid,elemid,marker=',')
        subplots['ax9'].set_xlim(39.5,45.5)
        subplots['ax9'].set_ylim(0,16.5)
        subplots['ax9'].set_title("Hodo: 4")

        subplots['ax10'].scatter(elemid,detid,marker=',')
        subplots['ax10'].set_xlim(79.5,117.5)
        subplots['ax10'].set_ylim(-1,8.5)
        subplots['ax10'].set_title("Prop Tube 2")





        self.figure.subplots_adjust(wspace=.4) 
        self.figure.subplots_adjust(hspace=1) 
        
        self.canvas.draw()

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
        layout = QVBoxLayout()
        self.setLayout(layout)


        self.data_reader = None
        self.plot_data = None
        self.previous_plot_data = None

        # #Momentum Plot
        # filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npy")])
        # self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MOMENTUM")
        # self.plot_data = self.data_reader.read_data()
        
        # self.momentumPlot = StaticHistogram(self.plot_data)
        # layout.addWidget(self.momentumPlot,1,0)

        
        #Hitmatrix Plot
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"HIT")
        self.plot_data = self.data_reader.read_data()
        self.hits = self.plot_data[1]
    
        num_events = 20 #len(hits)
        hitmatrix = np.zeros((num_events,1000,2))

        DriftChamber = np.zeros((num_events,4))
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



        # print((np.sum(DriftChamber[:,0]),np.sum(DriftChamber[:,1]),np.sum(DriftChamber[:,2]),np.sum(DriftChamber[:,3])))
        # print(np.sum(Hodoscope))
        # print(np.sum(propTube))
        # plt.scatter(hitmatrix[0,:,0],hitmatrix[0,:,1])
        # plt.xlim(-.5,6.5)
        # plt.show()
        # print(hitmatrix[hitmatrix[:,:,0] != 0][:,0])
        # plt.hist(hitmatrix[hitmatrix[:,:,1] != 0][:,0], bins=60, color='skyblue', edgecolor='black')
        # plt.xlim(-.5,6.5)
        # plt.show()


        # #n
        # self.event = 0
        self.hit_matrix_plotter = HitMatrixPlotter(hitmatrix)
        layout.addWidget(self.hit_matrix_plotter.canvas)
  
  
        


 

        # Add update button
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_plots)
        layout.addWidget(self.update_button)

       


    def update_plots(self):
        if self.data_reader:
            #self.previous_plot_data = self.plot_data.copy() if self.plot_data is not None else None
            self.data_reader.next_file()
            self.plot_data = self.data_reader.read_data()
            #self.histogram_plot = HistogramPlot(self.plot_data, self.previous_plot_data)
            layout = self.layout()
            layout.replaceWidget(layout.itemAt(0).widget(), self.momentumPlot)
            layout.addWidget(self.update_button)
            print("next plot")


class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(pg.ImageView())
        self.setLayout(layout)


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

        tabs.addTab(tab1, "Main Display")
        tabs.addTab(tab2, "Hit Information")
        self.setCentralWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
