import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton
import pyqtgraph as pg
import numpy as np
import uproot


class DataReader:
    def __init__(self, filenames):
        self.filenames = filenames
        self.current_index = 0

    def read_data(self):
        filename = self.filenames[self.current_index]
        targettree = uproot.open(filename)['QA_ana']
        gvx = targettree['gvx'].arrays(library='np')['gvx']
        gvy = targettree['gvy'].arrays(library='np')['gvy']
        gvz = targettree['gvz'].arrays(library='np')['gvz']

        vtx0 = [sublist[0] for sublist in gvx]
        vtx1 = [sublist[1] for sublist in gvx]
        vty0 = [sublist[0] for sublist in gvy]
        vty1 = [sublist[1] for sublist in gvy]
        vtz0 = [sublist[0] for sublist in gvz]
        vtz1 = [sublist[1] for sublist in gvz]

        vtx_data = np.array([vtx0, vtx1, vty0, vty1, vtz0, vtz1]).T
        return vtx_data
    
    def next_file(self):
        self.current_index = (self.current_index + 1) % len(self.filenames)


class HistogramPlot(QWidget):
    def __init__(self, vtx_data, previous_data=None):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.plot_widgets = []

        self.plot_data = vtx_data
        self.previous_plot_data = previous_data

        self.create_histograms()

    def create_histograms(self):
        for data, color in zip([self.plot_data, self.previous_plot_data], [(0, 0, 255, 150), (255, 0, 0, 150)]):
            plot_layout = QVBoxLayout()
            for i in range(3):
                plot_widget = pg.PlotWidget()
                hist, bins = np.histogram(data[:, i], bins=50)
                plot_widget.plot(bins, hist, stepMode=True, fillLevel=0, brush=color)
                plot_layout.addWidget(plot_widget)
                self.plot_widgets.append(plot_widget)
            self.layout().addLayout(plot_layout)


class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.data_reader = None
        self.plot_data = None
        self.previous_plot_data = None

        filenames = sorted([filename for filename in os.listdir("Data") if filename.endswith(".root")])
        self.data_reader = DataReader([os.path.join("Data", filename) for filename in filenames])
        self.plot_data = self.data_reader.read_data()

        self.histogram_plot = HistogramPlot(self.plot_data, np.zeros_like(self.plot_data))
        layout.addWidget(self.histogram_plot)

        # Add update button
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_plots)
        layout.addWidget(self.update_button)

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
