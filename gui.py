import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
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

        #add button for ploting values
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

    def show_aij(self, a_ij):
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
        a_ij.shape = (36,)

    def plot_event(self, button):
        a_ij = inf.calculate_aj()
        self.show_aij(a_ij)

        c = np.linspace(0, 200, 20)
        t = np.linspace(0, 100, 20)
        tk = np.zeros((20, 20), dtype=float)

        f = open("approximation.txt", "w")
        i = 0
        for c_val in c:
            j = 0
            for t_val in t:
                tk[i, j] = inf.tk_ct(a_ij, c_val, t_val)
                f.write("tk(c = "+ str(c_val) + ", t = "+ str(t_val) +") = " + str(tk[i , j]) + "; \n")
                j += 1
            i += 1
        f.close()

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # Make data.
        c, t = np.meshgrid(c, t)

        # Plot the surface.
        surf = ax.plot_surface(c, t, tk, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()