# Native Package | os
import os

# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

# Something | DataReader
from spinquest_gui.modules.calculations.DataReader import DataReader
from spinquest_gui.modules.directories.directory_health import get_reconstructed_directory

class MyTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 400, 300)

        # Insert data into the table

    def setData(self):
        print("=======MOM=======")
        print(mom)
        data = [
            ("Run ID", rid),
            ("Spill ID",  sid),
            #("Total Hits",  totalHits),
            # ("PX",round(meanPX,4)),
            # ("PY",round(meanPY,4)),
            # ("PZ",round(meanPZ,4))

            
        ]


        # Populate the table with data
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(str(value))
                self.setItem(row, col, item)