# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5.QtWidgets import QWidget

# External Packages | pyqtgraph
import pyqtgraph as pg

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