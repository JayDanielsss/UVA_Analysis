# External Packages | NumPy
import numpy as np
import os

# External Packages | PyQt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg

# Modules | HitDisplay
#from app.modules.HitDisplay import HitDisplay
from app.modules.HitDisplay import HitDisplay

from app.modules.DataOrganizer import DataOrganizer

class Tab1(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #layout = QVBoxLayout(self)  # Initialize the layout with the widget as parent
        #self.plot_widget = pg.PlotWidget()  # Create the plot widget
        #layout.addWidget(self.plot_widget)  # Add the plot widget to the layout

                # Create the first tab with the PlotWidget
        # Set up the layout for the widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        # Create QLabel for readout
        self.readout_label = QLabel(alignment=Qt.AlignLeft)
        self.layout.addWidget(self.readout_label)

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # Raw Directory with root files from detector
        path_to_raw_directory = os.path.join("app/data/raw")

        # Initialize seen files set
        self.seen_files = set(os.listdir(path_to_raw_directory))

        # Create an instance of dataOrganizer
        self.organizer = DataOrganizer()
        # Call tab displays
        self.tab()

        # Setup a timer to check for new files repeatedly
        self.file_check_timer = QTimer(self)
        self.file_check_timer.timeout.connect(lambda: self.check_new_files(path_to_raw_directory))
        self.file_check_timer.start(40000)  # Check for new files every 40 seconds

    def check_new_files(self, directory):
        '''Watches the raw directory for new files'''
        # Current set of files in the directory
        current_files = set(os.listdir(directory))
        
        # Check for new files
        new_files = current_files - self.seen_files
        
        if new_files:
            for file in new_files:
                print(f"New file detected: {file}")
            # Update the set of seen files
            self.seen_files.update(new_files)

            self.tab()

    def hit_display(self):
        '''creates the hit_display for the main window.'''
        elementid, detectorid, selectedEvents, sid, hits, eventID, track = self.organizer.grab_HitInfo()
        self.hit_display_instance = HitDisplay(elementid, detectorid, selectedEvents, sid, hits, eventID, track, self.layout)

    def tab(self):
        '''Calls all displays for the tab.'''
        # Reorganize data and update displays
        self.organizer.organizeData()
        self.hit_display()
