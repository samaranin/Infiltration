import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
import Infiltration as inf

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()  
        

    def initUI(self):
        #set status bar
        self.statusBar().showMessage('Ready')

        #create functional button and add event to it
        calculate_btn = QPushButton('Calculate', self)
        calculate_btn.clicked.connect(self.calculate_event)

        plot_btn = QPushButton('Plot', self)
        plot_btn.clicked.connect(self.plot_event)

        #add table widget
        self.tableResult = QTableWidget()

        #create layout for result table
        vboxTabelResult = QVBoxLayout()
        vboxTabelResult.addWidget(QLabel('Result: '))
        vboxTabelResult.addWidget(self.tableResult)

        #create horizontal layout for button and move it to right side
        contolButtons = QHBoxLayout()
        contolButtons.addStretch(1)
        contolButtons.addWidget(calculate_btn)
        contolButtons.addWidget(plot_btn)

        #join both layouts in one vertical
        vbox = QVBoxLayout()

        vbox.addLayout(vboxTabelResult)
        vbox.addLayout(contolButtons)

        #create new widget and add layout to it
        central_widget = QWidget()
        central_widget.setLayout(vbox) 

        #draw and show main window
        self.setCentralWidget(central_widget)
        self.setGeometry(150, 150, 550, 150)
        self.setWindowTitle('Soil Moisture')
        self.show()

    def calculate_event(self, button):
        a_ij = inf.calculate_aj()
        n = a_ij.shape[0]

        self.tableResult.setRowCount(1)
        self.tableResult.setColumnCount(n)
        for i in range(n):
            self.tableResult.setItem(0, i, QTableWidgetItem(str(a_ij[i])))

        self.statusBar().showMessage('Coefficeints Calculated')

        f = open("a_ij.txt", "w")
        a_ij.shape = (9, 4)
        f.write(str(a_ij))
        f.close

    def plot_event(self, button):
        pass