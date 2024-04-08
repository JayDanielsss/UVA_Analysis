import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QGridLayout
import pyqtgraph as pg
import numpy as np
from DataReader import DataReader


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
            
            plot_layout = QVBoxLayout()
            plot_widget = pg.PlotWidget()
            hist, bins = np.histogram(plot_data[:,0], bins=50)
            plot_widget.plot(bins, hist, stepMode=True, fillLevel=0, brush=color)
            plot_layout.addWidget(plot_widget)
            self.plot_widgets.append(plot_widget)
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
        layout = QGridLayout()
        self.setLayout(layout)

        self.data_reader = None
        self.plot_data = None
        self.previous_plot_data = None
        
        filenames = sorted([filename for filename in os.listdir("Data") if filename.endswith(".root")])
        self.data_reader = DataReader([os.path.join("Data", filename) for filename in filenames],"VERTEX")
        self.plot_data = self.data_reader.read_data()

        #self.histogram_plot = HistogramComparisonPlot(self.plot_data, np.zeros_like(self.plot_data))
        #layout.addWidget(self.histogram_plot)
        
        self.momentumPlot = StaticHistogram(self.plot_data)
        layout.addWidget(self.momentumPlot,0,0)

        self.momentumPlot2 = StaticHistogram(self.plot_data)
        layout.addWidget(self.momentumPlot2,3,0)

        # Add update button
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_plots)
        layout.addWidget(self.update_button,3,3)

    def update_plots(self):
        if self.data_reader:
            self.previous_plot_data = self.plot_data.copy() if self.plot_data is not None else None
            self.data_reader.next_file()
            self.plot_data = self.data_reader.read_data()
            self.histogram_plot = HistogramPlot(self.plot_data, self.previous_plot_data)

            layout = self.layout()
            layout.replaceWidget(layout.itemAt(0).widget(), self.histogram_plot)
            layout.addWidget(self.update_button)

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

        tabs.addTab(tab1, "Vtx Information")
        tabs.addTab(tab2, "Hit Information")
        self.setCentralWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
