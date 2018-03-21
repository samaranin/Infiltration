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

        self.c_min_edit = QLineEdit('0')
        self.c_max_edit = QLineEdit('200')
        self.t_min_edit = QLineEdit('0')
        self.t_max_edit = QLineEdit('100')
        self.step = QLineEdit('50')

        #add table widget
        self.tableResult = QTableWidget()

        #create layout for result table
        vboxTabelResult = QVBoxLayout()
        vboxTabelResult.addWidget(QLabel('Aij Coefficients: '))
        vboxTabelResult.addWidget(self.tableResult)

        #create horizontal layout for button and move it to right side
        contolButtons = QHBoxLayout()
        contolButtons.addStretch(1)
        contolButtons.addWidget(plot_btn)

        #grid for labels
        gridNet = QGridLayout()
        gridNet.setSpacing(10)

        gridNet.addWidget(QLabel('C Min ='), 1, 0)
        gridNet.addWidget(self.c_min_edit, 1, 1)

        gridNet.addWidget(QLabel('C Max = '), 1, 2)
        gridNet.addWidget(self.c_max_edit, 1, 3)

        gridNet.addWidget(QLabel('T Min = '), 2, 0)
        gridNet.addWidget(self.t_min_edit, 2, 1)
            
        gridNet.addWidget(QLabel('T Max = '), 2, 2)
        gridNet.addWidget(self.t_max_edit, 2, 3) 

        gridNet.addWidget(QLabel('Discretization Step = '), 3, 0)
        gridNet.addWidget(self.step,3, 1) 

        #join both layouts in one vertical
        vbox = QVBoxLayout()
        vbox.addLayout(gridNet)
        vbox.addWidget(QHLine())

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

        step = int(self.step.text())
        c = np.linspace(float(self.c_min_edit.text()), float(self.c_max_edit.text()), step)
        t = np.linspace(float(self.t_min_edit.text()), float(self.t_max_edit.text()), step)
        tk = np.zeros((step, step), dtype=float)

        f = open("approximation.txt", "w")
        i = 0
        for c_val in c:
            j = 0
            for t_val in t:
                tk[i, j] = inf.tk_ct(a_ij, c_val, t_val)
                f.write("tk("+ str(c_val) + ", "+ str(t_val) +") = " + str(tk[i , j]) + "\n")
                j += 1
            i += 1
        f.close()

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        # Make data.
        c, t = np.meshgrid(c, t)
        # Plot the surface.
        surf = ax.plot_surface(c, t, tk, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        # Customize the z axis.
        ax.set_zlim(tk.min(), tk.max())
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=1, aspect=5)
        plt.show()

        self.statusBar().showMessage('Approximation ploted')