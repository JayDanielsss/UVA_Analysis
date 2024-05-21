# class StripChartWindow(QWidget):

#     def __init__(self):

#         super().__init__()

#         layout = QVBoxLayout()  # Create one QVBoxLayout

#         layout.addWidget(self.txtBox)
#         self.setLayout(layout)


# class StripChartWindow(QMainWindow):
 
#     def __init__(self):
#         super().__init__()
#         self.title = 'SpinQuest Display'
#         self.left = 0
#         self.top = 0
#         self.width = 800
#         self.height = 400
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
        
#         tabs = QTabWidget()
#         tab2 = Tab2()
#         tabs.addTab(tab2, "StripCharts")
#         self.setCentralWidget(tabs)
