#####################
### SpinQuest GUI ###
###  Jay, S, M, D   ###
#####################

# Native Package | sys
import sys
import os

# External Packages | PyQt5
from PyQt5.QtWidgets import QMainWindow,QApplication, QTabWidget

# from spinquest_gui.plots.MassHist import MassHist

from app.tabs.tab1 import Tab1



from app.modules.constants import _APPLICATION_NAME, _WINDOW_MAIN_APP_WIDTH, _WINDOW_MAIN_APP_HEIGHT

# from spinquest_gui.plots.StripChartsWindow import StripChartWindow

# PyQT Window | Main Window
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget

class App(QMainWindow):

    def __init__(self):
        
        super().__init__()
        

        # Set the name of the application:
        self.title = _APPLICATION_NAME
        self.setWindowTitle(self.title)

        # Configure the geometry of the application window:
        self.window_left = 0
        self.window_top = 0
        self.window_width = _WINDOW_MAIN_APP_WIDTH
        self.window_height = _WINDOW_MAIN_APP_HEIGHT
        self.setGeometry(self.window_left, self.window_top, self.window_width, self.window_height)

        # Initalize additional UI:
    
        self.initializeUI()

    def initializeUI(self):

        # # Initialize PyQT's "central widget"
        # self.central_widget = QTabWidget()
        # self.setCentralWidget(self.central_widget)

        # Initialize the central widget's tabs:
        # self.tab1 = Tab1()

        tab_widget = QTabWidget()


        tab1_instance = Tab1()
        
        #tab2 = Tab2()
        # tab2 = MassHist()

        #self.central_widget.addTab(tab1, "Main Display")
        tab_widget.addTab(tab1_instance,"Main Display")
        self.setCentralWidget(tab_widget)
       # self.central_widget.addTab(tab2, "Strip Charts")
        # self.central_widget.addTab(tab2,"Mass Histogram")
        
       # tabs.addTab(tab3, "Spill")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()

    # window2 = StripChartWindow()
    # window2.show()
    sys.exit(app.exec_())
