#=====================
#=======Jay===========
#=====================

# External Packages | NumPy
import numpy as np

# External Packages 
import pyqtgraph as pg
from PyQt5.QtCore import QObject

class MassDisplay(QObject):
    def __init__(self, layout, mass, selected_events):
        super().__init__()  # Call the constructor of QObject

        self.layout = layout
        self.mass = mass
        self.selected_events = selected_events

        grid_layout = pg.GraphicsLayoutWidget()
        per_spill_grid = grid_layout.addPlot(1, 1)
        self.display_per_spill(per_spill_grid)

        # Add the grid layout to the widget layout
        self.layout.addWidget(grid_layout)

    def display_per_spill(self, plot_widget):
        print("TESTING!")
        # Create histogram data
        y, x = np.histogram(self.mass, bins=80)
        
        # Create a bar graph item and add it to the plot
        bg = pg.BarGraphItem(x=x[:-1], height=y, width=x[1]-x[0], brush='r')
        plot_widget.addItem(bg)
        
        # Set labels
        plot_widget.setLabel('left', 'Frequency')
        plot_widget.setLabel('bottom', 'Value')
        
        # Set title
        plot_widget.setTitle('Histogram Example')
