import os
from configparser import ConfigParser

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def getFileDialogFilter():
    return 'Content (*.json);;All files (*)'


def getFileDialogDirectory():
    return 'fixpointtool/content'


ALGEBRA_LIST = ["algebra 1", "algebra 2"]


class FPTSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.resize(300, 100)

        # self.content_directory_label = QLabel("Content directory:")
        self.mv_algebra_label = QLabel("MV-algebra:")
        self.mv_algebra_k_label = QLabel("k:")
        self.mv_algebra_k_label.setMinimumWidth(135)
        sp = self.mv_algebra_k_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.mv_algebra_k_label.setSizePolicy(sp)

        # self.content_directory_button = QPushButton("...")
        # self.content_directory_button.setDefault(False)
        # self.content_directory_button.setAutoDefault(False)
        # self.content_directory_button.clicked.connect(self.onContentDirectoryButtonClicked)
        # self.content_directory_button.setObjectName("content_directory_button")

        self.mv_algebra_comboBox = QComboBox()
        self.mv_algebra_comboBox.addItems(ALGEBRA_LIST)
        self.mv_algebra_comboBox.setItemData(0, "( [0, 1], \u2A01, 0, \u0304·\u0304 )\n"
                                                "x \u2A01 y = min{x + y, 1}\n"
                                                "x\u0304 = 1 - x", Qt.ToolTipRole)
        self.mv_algebra_comboBox.setItemData(1, "( {0,...,k}, \u2A01, 0, \u0304·\u0304 )\n"
                                                "x \u2A01 y = min{x + y, k}\n"
                                                "x\u0304 = k - x", Qt.ToolTipRole)
        # self.mv_algebra_comboBox.currentIndexChanged.connect(self.onMVAlgebraChanged)

        self.mv_algebra_k_lineEdit = QLineEdit()
        onlyInt = QIntValidator(1, 99999)
        self.mv_algebra_k_lineEdit.setValidator(onlyInt)

        self.mv_algebra_k_lineEdit.textChanged.connect(lambda text: self.fixKValue(self.mv_algebra_k_lineEdit, text))

        # self.content_directory_box = QHBoxLayout()
        # self.content_directory_box.addWidget(self.content_directory_label)
        # self.content_directory_box.addWidget(self.content_directory_button)

        self.mv_algebra_box = QHBoxLayout()
        self.mv_algebra_box.addWidget(self.mv_algebra_label)
        self.mv_algebra_box.addWidget(self.mv_algebra_comboBox)

        self.mv_algebra_k_box = QHBoxLayout()
        self.mv_algebra_k_box.addWidget(self.mv_algebra_k_label)
        self.mv_algebra_k_box.addWidget(self.mv_algebra_k_lineEdit)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.setDefault(False)
        self.save_button.setAutoDefault(False)
        self.cancel_button.setDefault(False)
        self.cancel_button.setAutoDefault(False)
        self.save_button.clicked.connect(self.onSave)
        self.cancel_button.clicked.connect(self.onCancel)

        self.save_cancel_box = QHBoxLayout()
        self.save_cancel_box.addWidget(self.save_button)
        self.save_cancel_box.addWidget(self.cancel_button)

        self.vbox = QVBoxLayout()
        # self.vbox.addLayout(self.content_directory_box)
        self.vbox.addLayout(self.mv_algebra_box)
        self.vbox.addLayout(self.mv_algebra_k_box)
        self.vbox.addStretch()
        self.vbox.addLayout(self.save_cancel_box)

        self.readConfig()

        # self.mv_algebra_k_label.setVisible(self.mv_algebra_comboBox.currentText() == "algebra 2")
        # self.mv_algebra_k_lineEdit.setVisible(self.mv_algebra_comboBox.currentText() == "algebra 2")

        self.setLayout(self.vbox)

    def fixKValue(self, input, text):
        if "." in text:
            input.setText(text.replace(".", ""))

    def readConfig(self):
        config = ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

        # self.content_directory_button.setText(config['all']['content'])
        if config['all']['mv-algebra'] in ALGEBRA_LIST:
            self.mv_algebra_comboBox.setCurrentText(config['all']['mv-algebra'])
        else:
            print("WARNING: mv-algebra does not exist (default: algebra 1)")
        try:
            if 0 < int(config['all']['k']) < 100000:
                self.mv_algebra_k_lineEdit.setText(config['all']['k'])
            else:
                self.mv_algebra_k_lineEdit.setText(1)
                print("WARNING: k is negative or too big (>99999) (default: 1)")
        except ValueError as e:
            self.mv_algebra_k_lineEdit.setText(1)
            print("WARNING: k is no integer (default: 1)")

#     def onMVAlgebraChanged(self):
#         self.mv_algebra_k_label.setVisible(self.mv_algebra_comboBox.currentText() == "algebra 2")
#         self.mv_algebra_k_lineEdit.setVisible(self.mv_algebra_comboBox.currentText() == "algebra 2")

    # def onContentDirectoryButtonClicked(self):
    #     fname, filter = QFileDialog.getOpenFileName(self, "Choose content directory",
    #                                                 getFileDialogDirectory(), getFileDialogFilter())
    #     if fname != "" and os.path.isfile(fname):
    #         self.content_directory_button.setText(os.path.basename(fname))

    def onSave(self):
        if self.mv_algebra_k_lineEdit.text() == "":
            self.mv_algebra_k_lineEdit.setText(str(1))
        self.accept()

    def onCancel(self):
        self.reject()
