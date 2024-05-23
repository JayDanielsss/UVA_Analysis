# Native Package | os
import os

# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QTimer

# External Packages | pyqtgraph
import pyqtgraph as pg

# Something | DataReader
from spinquest_gui.modules.calculations.DataOrganizer import DataOrganizer

# Something | StripCharts
from spinquest_gui.plots.OrganizerMassHist import OrgMassHist

# Physics

### Lorentz Dot Product
from spinquest_gui.modules.physics.calculate_physics import lorentz_dot_product

class Tab2(QWidget):
    def __init__(self, organizer : DataOrganizer):
        super().__init__()
        layout = QVBoxLayout()
        
        self.setLayout(layout)

        vertexStrip_layout = QVBoxLayout()
        
        self.hist = OrgMassHist(organizer)
        vertexStrip_layout.addWidget(self.hist)


        layout.addLayout(vertexStrip_layout,stretch = 4)

    def refresh_modules(self, organizer : DataOrganizer):
        self.hist.drawHist(organizer)