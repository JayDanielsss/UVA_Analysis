# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5.QtWidgets import QWidget, QHBoxLayout

# External Packages | pyqtgraph
import pyqtgraph as pg

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