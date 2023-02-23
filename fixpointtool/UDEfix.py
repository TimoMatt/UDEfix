import os
import sys
from PyQt5.QtWidgets import *

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fixpointtool.fpt_window import FPTWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    wnd = FPTWindow()
    wnd.show()

    wnd.onFileNew()  # start with a new File opened

    sys.exit(app.exec_())