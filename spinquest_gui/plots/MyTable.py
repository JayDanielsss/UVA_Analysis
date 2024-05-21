# Native Package | os
import os

# External Packages | NumPy
import numpy as np

# External Packages | PyQTt5
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

# Something | DataReader
from spinquest_gui.modules.calculations.DataReader import DataReader

class MyTable(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.setGeometry(0, 0, 400, 300)

        # Insert data into the table

    def setData(self,fileNumber):

        #Direct Data
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MetaDATA")
        self.data_reader.current_index = fileNumber
        self.plot_data = self.data_reader.read_data()

        # #Momentum
        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MOMENTUM")
        self.data_reader.current_index = fileNumber
        self.plot_data = self.data_reader.read_data()
        meanPX = np.mean(self.plot_data[0])
        meanPY = np.mean(self.plot_data[1])
        meanPZ = np.mean(self.plot_data[2])
        totalHits = self.plot_data[3]

        del(self.plot_data)

        filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npz")])
        self.data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MetaDATA")
        self.data_reader.current_index = fileNumber
        self.plot_data = self.data_reader.read_data()
        RunID = self.plot_data[0][0]
        SpillID = self.plot_data[1][0]

        data = [
            ("Run ID", RunID),
            ("Spill ID",  SpillID),
            ("Total Hits",  totalHits),
            ("PX",round(meanPX,4)),
            ("PY",round(meanPY,4)),
            ("PZ",round(meanPZ,4))

            
        ]


        # Populate the table with data
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(str(value))
                self.setItem(row, col, item)