from PyQt5 import QtWidgets
from gpu_viewer_gui import GPUViewerApp
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = GPUViewerApp()
    win.show()
    sys.exit(app.exec_())
