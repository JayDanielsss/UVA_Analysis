# Native Package | os
import os

# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

# External Packages | pyqtgraph
import pyqtgraph as pg

class HitMatrixPlotter(QWidget):

    def __init__(
            self, 
            hitmatrix,
            Station,
            Plane,
            x_range = None,
            y_range = None,
            Title = None):

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
        csv_path = os.path.join(current_dir, '..', 'statics', 'geometry.csv')

        geometery = np.loadtxt(csv_path, delimiter = ",", dtype = str)
        
        PerEvent = np.zeros_like(detector)
        
        for i in range(len(detector)):
            for j in range(len(detector[0])):
                PerEvent[i,j] = detector[i,j]/int(geometery[Plane[j]][1])

        AvgOccPerSpill = np.average(PerEvent)
        TotalOccPerSpill = np.sum(detector)

        text = f"Occupancy\nAvg Hits per Event: {AvgOccPerSpill*100:.0f}%\nTotal Hits per Spill: {TotalOccPerSpill}\n"
        self.readout_label.setText(text)