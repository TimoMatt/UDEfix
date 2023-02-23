from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class TypesButton(QPushButton):
    def __init__(self, txt, i, popup):
        super().__init__(text=txt)

        self.index = i
        self.popup = popup

        self.clicked.connect(lambda: QDMContentListWidgetTupleTypePopup.onButtonClicked(self.popup, self.index))


class QDMContentListWidgetTupleTypePopup(QDialog):
    LIST_OF_INNER_TYPES = ["string", "number"]
    LIST_OF_TUPLE_TYPES = ["string", "number", "mapping", "n-tuple", "set"]

    def __init__(self, types_of_tuple, inner=False, parent=None):
        super().__init__(parent)
        try:
            self.types_of_tuple = types_of_tuple
            self.n = len(types_of_tuple)
            self.inner = inner

            self.setWindowTitle("Edit tuple types")
            self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
            self.resize(200, 10)

            self.types_label = QLabel("Types:")

            self.vbox = QVBoxLayout()
            self.vbox.addWidget(self.types_label)

            self.type_comboBoxes = []
            self.n_labels = []
            self.n_lineEdits = []
            self.tuple_labels = []
            self.tuple_buttons = []
            self.set_labels = []
            self.set_comboBoxes = []

            for i in range(self.n):
                current_type = self.types_of_tuple[i]
                current_tuple_types = None
                current_set_type = None
                if type(current_type) == tuple and current_type[0] == "n-tuple":
                    current_tuple_types = current_type[1]
                elif type(current_type) == tuple and current_type[0] == "set":
                    current_set_type = current_type[1]

                lbl = QLabel(str(i+1) + ":")
                lbl.setMargin(4)

                typ = QComboBox()
                typ.addItems(QDMContentListWidgetTupleTypePopup.LIST_OF_TUPLE_TYPES if not self.inner else QDMContentListWidgetTupleTypePopup.LIST_OF_INNER_TYPES)
                if current_tuple_types is None and current_set_type is None:
                    typ.setCurrentText(current_type)
                else:
                    typ.setCurrentText(current_type[0])
                self.type_comboBoxes.append(typ)

                hbox = QHBoxLayout()
                hbox.addWidget(lbl)
                hbox.addWidget(typ)

                if not self.inner:
                    onlyInt = QIntValidator(2, 9)

                    n_lbl = QLabel("n:")
                    n_lbl.setMargin(8)
                    n_lbl.setMinimumWidth(86)
                    self.n_labels.append(n_lbl)

                    sp = n_lbl.sizePolicy()
                    sp.setHorizontalPolicy(QSizePolicy.Expanding)
                    n_lbl.setSizePolicy(sp)

                    n_le = QLineEdit()
                    n_le.setValidator(onlyInt)
                    n_le.setText("2")
                    if current_tuple_types is not None:
                        n_le.setText(str(len(current_tuple_types)))
                    self.n_lineEdits.append(n_le)

                    tuple_lbl = QLabel("Types:")
                    tuple_lbl.setMargin(8)
                    self.tuple_labels.append(tuple_lbl)

                    tuple_btn = TypesButton("Edit", i, self)
                    tuple_btn.setDefault(False)
                    tuple_btn.setAutoDefault(False)
                    self.tuple_buttons.append(tuple_btn)

                    n_lbl.setVisible(current_tuple_types is not None)
                    n_le.setVisible(current_tuple_types is not None)
                    tuple_lbl.setVisible(current_tuple_types is not None)
                    tuple_btn.setVisible(current_tuple_types is not None)

                    n_hbox = QHBoxLayout()
                    n_hbox.addWidget(n_lbl)
                    n_hbox.addWidget(n_le)

                    tuple_hbox = QHBoxLayout()
                    tuple_hbox.addWidget(tuple_lbl)
                    tuple_hbox.addWidget(tuple_btn)

                    set_lbl = QLabel("Type:")
                    set_lbl.setMargin(8)
                    self.set_labels.append(set_lbl)

                    set_cb = QComboBox()
                    set_cb.addItems(QDMContentListWidgetTupleTypePopup.LIST_OF_INNER_TYPES)
                    if current_set_type is not None:
                        set_cb.setCurrentText(current_type[1])
                    else:
                        set_cb.setCurrentText("string")
                    self.set_comboBoxes.append(set_cb)

                    set_lbl.setVisible(current_set_type is not None)
                    set_cb.setVisible(current_set_type is not None)

                    set_hbox = QHBoxLayout()
                    set_hbox.addWidget(set_lbl)
                    set_hbox.addWidget(set_cb)

                    typ.currentTextChanged.connect(self.updateVisibility)

                box = QVBoxLayout()
                box.setContentsMargins(0, 0, 0, 10)
                box.addLayout(hbox)
                if not self.inner:
                    box.addLayout(n_hbox)
                    box.addLayout(tuple_hbox)
                    box.addLayout(set_hbox)
                self.vbox.addLayout(box)

            self.save_button = QPushButton("Save")
            self.cancel_button = QPushButton("Cancel")
            self.save_button.setDefault(False)
            self.save_button.setAutoDefault(False)
            self.cancel_button.setDefault(False)
            self.cancel_button.setAutoDefault(False)
            self.save_button.clicked.connect(self.onSave)
            self.cancel_button.clicked.connect(self.onCancel)

            self.hbox = QHBoxLayout()
            self.hbox.addWidget(self.save_button)
            self.hbox.addWidget(self.cancel_button)
            self.vbox.addLayout(self.hbox)

            self.setLayout(self.vbox)
        except Exception as e:
            print(e)

    def onButtonClicked(self, i):
        try:
            current_n = self.n_lineEdits[i].text()
            if current_n == "0" or current_n == "1" or current_n == "":
                self.n_lineEdits[i].setText("2")
                current_n = "2"
            if self.types_of_tuple[i][0] != "n-tuple" or len(self.types_of_tuple[i][1]) != int(self.n_lineEdits[i].text()):
                self.types_of_tuple[i] = tuple(["n-tuple", ["string"]*int(current_n)])
            pop = QDMContentListWidgetTupleTypePopup(self.types_of_tuple[i][1], inner=True)
            if pop.exec():
                self.types_of_tuple[i] = tuple(["n-tuple", pop.types_of_tuple])
        except Exception as e:
            print(e)

    def updateVisibility(self):
        for i in range(self.n):
            current_type = self.type_comboBoxes[i].currentText()

            self.n_labels[i].setVisible(current_type == "n-tuple")
            self.n_lineEdits[i].setVisible(current_type == "n-tuple")
            self.tuple_labels[i].setVisible(current_type == "n-tuple")
            self.tuple_buttons[i].setVisible(current_type == "n-tuple")
            self.set_labels[i].setVisible(current_type == "set")
            self.set_comboBoxes[i].setVisible(current_type == "set")

        self.resize(200, 10)

    def onSave(self):
        if self.inner:
            self.types_of_tuple = []
            for elem in self.type_comboBoxes:
                self.types_of_tuple.append(elem.currentText())
        else:
            for i in range(self.n):
                current_type = self.type_comboBoxes[i].currentText()

                if current_type == "string" or current_type == "number" or current_type == "mapping":
                    self.types_of_tuple[i] = current_type
                elif current_type == "n-tuple":
                    if self.types_of_tuple[i][0] != "n-tuple":
                        current_n = self.n_lineEdits[i].text()
                        if current_n == "0" or current_n == "1" or current_n == "":
                            self.n_lineEdits[i].setText("2")
                            current_n = "2"
                        self.types_of_tuple[i] = tuple(["n-tuple", ["string"]*int(current_n)])
                elif current_type == "set":
                    self.types_of_tuple[i] = tuple(["set", self.set_comboBoxes[i].currentText()])

        self.accept()

    def onCancel(self):
        self.reject()