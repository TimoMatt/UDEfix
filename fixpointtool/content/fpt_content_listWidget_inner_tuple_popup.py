from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.content.fpt_content_listWidgetItem import QDMListWidgetItem
from fixpointtool.content.fpt_mapping import FPTMapping


class QDMContentListWidgetTuplePopup(QDialog):
    LIST_OF_INNER_TUPLE_TYPES = ["string", "number"]
    LIST_OF_INNER_SET_TYPES = ["string", "number"]

    def __init__(self, tup, type_of_tuple, editing=False, excluded_mapping=None, parent=None):
        super().__init__(parent)

        self.tuple = tup
        self.type_of_tuple = type_of_tuple

        self.setWindowTitle("Edit tuple")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.resize(300, 100)

        self.accessDicts = AccessDictionaries()

        self.type_label = QLabel("Type:")

        self.firstTupleType_label = QLabel("First tuple type")
        self.secondTupleType_label = QLabel("Second tuple type")
        self.firstTupleType_label.setMargin(4)
        self.secondTupleType_label.setMargin(4)

        self.firstTupleType_comboBox = QComboBox()
        self.secondTupleType_comboBox = QComboBox()
        self.firstTupleType_comboBox.addItems(QDMContentListWidgetTuplePopup.LIST_OF_INNER_TUPLE_TYPES)
        self.secondTupleType_comboBox.addItems(QDMContentListWidgetTuplePopup.LIST_OF_INNER_TUPLE_TYPES)

        self.firstTupleTypeBox = QHBoxLayout()
        self.secondTupleTypeBox = QHBoxLayout()

        self.firstTupleTypeBox.addWidget(self.firstTupleType_label)
        self.firstTupleTypeBox.addWidget(self.firstTupleType_comboBox)
        self.secondTupleTypeBox.addWidget(self.secondTupleType_label)
        self.secondTupleTypeBox.addWidget(self.secondTupleType_comboBox)

        if self.type_of_tuple == "2-tuple":
            if type(self.tuple[0][0]) == str:
                self.firstTupleType_comboBox.setCurrentText("string")
            elif type(self.tuple[0][0]) == int or type(self.tuple[0][0]) == float:
                self.firstTupleType_comboBox.setCurrentText("number")
            else:
                print("WARNING: Inner tuple type is not supported")
            if type(self.tuple[1][0]) == str:
                self.secondTupleType_comboBox.setCurrentText("string")
            elif type(self.tuple[1][0]) == int or type(self.tuple[1][0]) == float:
                self.secondTupleType_comboBox.setCurrentText("number")
            else:
                print("WARNING: Inner tuple type is not supported")

        self.firstTupleType_comboBox.currentIndexChanged.connect(self.firstTupleTypeChanged)
        self.secondTupleType_comboBox.currentIndexChanged.connect(self.secondTupleTypeChanged)

        self.firstSetType_label = QLabel("First set type")
        self.secondSetType_label = QLabel("Second set type")
        self.firstSetType_label.setMargin(4)
        self.secondSetType_label.setMargin(4)

        self.firstSetType_comboBox = QComboBox()
        self.secondSetType_comboBox = QComboBox()
        self.firstSetType_comboBox.addItems(QDMContentListWidgetTuplePopup.LIST_OF_INNER_SET_TYPES)
        self.secondSetType_comboBox.addItems(QDMContentListWidgetTuplePopup.LIST_OF_INNER_SET_TYPES)

        self.firstSetTypeBox = QHBoxLayout()
        self.secondSetTypeBox = QHBoxLayout()

        self.firstSetTypeBox.addWidget(self.firstSetType_label)
        self.firstSetTypeBox.addWidget(self.firstSetType_comboBox)
        self.secondSetTypeBox.addWidget(self.secondSetType_label)
        self.secondSetTypeBox.addWidget(self.secondSetType_comboBox)

        if self.type_of_tuple == "set":
            for elem in self.tuple[0]:
                if type(elem) == str:
                    self.firstSetType_comboBox.setCurrentText("string")
                    break
                elif type(elem) == int or type(elem) == float:
                    self.firstSetType_comboBox.setCurrentText("number")
                    break
                else:
                    print("WARNING: Inner set type is not supported")
                    break
            for elem in self.tuple[1]:
                if type(elem) == str:
                    self.secondSetType_comboBox.setCurrentText("string")
                    break
                elif type(elem) == int or type(elem) == float:
                    self.secondSetType_comboBox.setCurrentText("number")
                    break
                else:
                    print("WARNING: Inner set type is not supported")
                    break

        self.firstSetType_comboBox.currentIndexChanged.connect(self.firstSetTypeChanged)
        self.secondSetType_comboBox.currentIndexChanged.connect(self.secondSetTypeChanged)

        self.content_label = QLabel("Content:")

        self.x_label = QLabel("First value:")
        self.x_label.setMinimumWidth(80)
        self.x_label.setMargin(4)
        self.y_label = QLabel("Second value:")
        self.y_label.setMinimumWidth(80)
        self.y_label.setMargin(4)

        self.x_value = QTextEdit()
        self.x_value.setText(str(self.tuple[0]))
        self.x_value.setMaximumHeight(23)
        self.y_value = QTextEdit()
        self.y_value.setText(str(self.tuple[1]))
        self.y_value.setMaximumHeight(23)

        mappings = list(self.accessDicts.getDictionaryWithoutTransformation("mappings").keys())
        if excluded_mapping is not None:
            mappings.pop(mappings.index(excluded_mapping))
        self.x_mapping = QComboBox()
        self.x_mapping.setMaximumHeight(23)
        self.x_mapping.addItems(mappings)
        if self.tuple[0] is not None and type(self.tuple[0]) == FPTMapping:
            self.x_mapping.setCurrentText(self.tuple[0].name)
        self.y_mapping = QComboBox()
        self.y_mapping.setMaximumHeight(23)
        self.y_mapping.addItems(mappings)
        if self.tuple[1] is not None and type(self.tuple[1]) == FPTMapping:
            self.y_mapping.setCurrentText(self.tuple[1].name)

        self.x_tuple = QListWidget()
        self.x_tuple.setMaximumHeight(24)
        self.x_tuple_add = QPushButton("+")
        self.x_tuple_add.setFixedHeight(23)
        self.x_tuple_add.setFixedWidth(23)
        self.x_tuple_add.setDefault(False)
        self.x_tuple_add.setAutoDefault(False)
        self.x_tuple_add.clicked.connect(self.addXTuple)

        self.x_tuple.itemDoubleClicked.connect(self.launchXPopup)

        self.y_tuple = QListWidget()
        self.y_tuple.setMaximumHeight(24)
        self.y_tuple_add = QPushButton("+")
        self.y_tuple_add.setFixedHeight(23)
        self.y_tuple_add.setFixedWidth(23)
        self.y_tuple_add.setDefault(False)
        self.y_tuple_add.setAutoDefault(False)
        self.y_tuple_add.clicked.connect(self.addYTuple)

        self.y_tuple.itemDoubleClicked.connect(self.launchYPopup)

        self.x_set = QListWidget()
        self.x_set.setMaximumHeight(24)
        self.x_set_add = QPushButton("+")
        self.x_set_add.setFixedHeight(23)
        self.x_set_add.setFixedWidth(23)
        self.x_set_add.setDefault(False)
        self.x_set_add.setAutoDefault(False)
        self.x_set_add.clicked.connect(self.addXSet)

        self.x_set.itemDoubleClicked.connect(self.launchXSetPopup)

        self.y_set = QListWidget()
        self.y_set.setMaximumHeight(24)
        self.y_set_add = QPushButton("+")
        self.y_set_add.setFixedHeight(23)
        self.y_set_add.setFixedWidth(23)
        self.y_set_add.setDefault(False)
        self.y_set_add.setAutoDefault(False)
        self.y_set_add.clicked.connect(self.addYSet)

        self.y_set.itemDoubleClicked.connect(self.launchYSetPopup)

        self.xBox = QHBoxLayout()
        self.yBox = QHBoxLayout()

        self.xBox.addWidget(self.x_label)
        self.xBox.addWidget(self.x_value)
        self.xBox.addWidget(self.x_mapping)
        self.xBox.addWidget(self.x_tuple)
        self.xBox.addWidget(self.x_tuple_add)
        self.xBox.addWidget(self.x_set)
        self.xBox.addWidget(self.x_set_add)
        self.yBox.addWidget(self.y_label)
        self.yBox.addWidget(self.y_value)
        self.yBox.addWidget(self.y_mapping)
        self.yBox.addWidget(self.y_tuple)
        self.yBox.addWidget(self.y_tuple_add)
        self.yBox.addWidget(self.y_set)
        self.yBox.addWidget(self.y_set_add)

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

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.type_label)
        self.vbox.addLayout(self.firstTupleTypeBox)
        self.vbox.addLayout(self.secondTupleTypeBox)
        self.vbox.addLayout(self.firstSetTypeBox)
        self.vbox.addLayout(self.secondSetTypeBox)
        self.vbox.addWidget(self.content_label)
        self.vbox.addLayout(self.xBox)
        self.vbox.addLayout(self.yBox)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.type_label.setVisible(self.type_of_tuple == "2-tuple" or self.type_of_tuple == "set")
        self.firstTupleType_label.setVisible(self.type_of_tuple == "2-tuple")
        self.firstTupleType_comboBox.setVisible(self.type_of_tuple == "2-tuple")
        self.secondTupleType_label.setVisible(self.type_of_tuple == "2-tuple")
        self.secondTupleType_comboBox.setVisible(self.type_of_tuple == "2-tuple")
        self.firstSetType_label.setVisible(self.type_of_tuple == "set")
        self.firstSetType_comboBox.setVisible(self.type_of_tuple == "set")
        self.secondSetType_label.setVisible(self.type_of_tuple == "set")
        self.secondSetType_comboBox.setVisible(self.type_of_tuple == "set")

        self.x_value.setVisible(self.type_of_tuple == "string" or self.type_of_tuple == "number")
        self.x_tuple.setVisible(self.type_of_tuple == "2-tuple")
        self.x_tuple_add.setVisible(self.type_of_tuple == "2-tuple")
        self.x_set.setVisible(self.type_of_tuple == "set")
        self.x_set_add.setVisible(self.type_of_tuple == "set")
        self.y_value.setVisible(self.type_of_tuple == "string" or self.type_of_tuple == "number")
        self.y_tuple.setVisible(self.type_of_tuple == "2-tuple")
        self.y_tuple_add.setVisible(self.type_of_tuple == "2-tuple")
        self.y_set.setVisible(self.type_of_tuple == "set")
        self.y_set_add.setVisible(self.type_of_tuple == "set")
        self.x_mapping.setVisible(self.type_of_tuple == "mapping")
        self.y_mapping.setVisible(self.type_of_tuple == "mapping")

        if editing and self.type_of_tuple == "2-tuple":
            tup1 = QDMListWidgetItem(self.tuple[0], "2-tuple")
            tup2 = QDMListWidgetItem(self.tuple[1], "2-tuple")
            self.x_tuple.addItem(tup1)
            self.y_tuple.addItem(tup2)
            self.x_tuple_add.setVisible(False)
            self.y_tuple_add.setVisible(False)
        if editing and self.type_of_tuple == "set":
            set1 = QDMListWidgetItem(self.tuple[0], "set")
            set2 = QDMListWidgetItem(self.tuple[1], "set")
            self.x_set.addItem(set1)
            self.y_set.addItem(set2)
            self.x_set_add.setVisible(False)
            self.y_set_add.setVisible(False)

    def firstTupleTypeChanged(self):
        self.x_tuple.clear()
        self.x_tuple_add.setVisible(True)

    def secondTupleTypeChanged(self):
        self.y_tuple.clear()
        self.y_tuple_add.setVisible(True)

    def firstSetTypeChanged(self):
        self.x_set.clear()
        self.x_set_add.setVisible(True)

    def secondSetTypeChanged(self):
        self.y_set.clear()
        self.y_set_add.setVisible(True)

    def launchXPopup(self, item):
        pop = QDMContentListWidgetTuplePopup(item.item, self.firstTupleType_comboBox.currentText())
        if pop.exec():
            item.item = pop.tuple
            item.overwriteText()

    def launchYPopup(self, item):
        pop = QDMContentListWidgetTuplePopup(item.item, self.secondTupleType_comboBox.currentText())
        if pop.exec():
            item.item = pop.tuple
            item.overwriteText()

    def launchXSetPopup(self, item):
        from fixpointtool.content.fpt_content_listWidget_inner_set_popup import QDMContentListWidgetInnerSetPopup
        pop = QDMContentListWidgetInnerSetPopup(item.item, self.firstSetType_comboBox.currentText())
        if pop.exec():
            item.item = pop.set
        item.overwriteText()

    def launchYSetPopup(self, item):
        from fixpointtool.content.fpt_content_listWidget_inner_set_popup import QDMContentListWidgetInnerSetPopup
        pop = QDMContentListWidgetInnerSetPopup(item.item, self.secondSetType_comboBox.currentText())
        if pop.exec():
            item.item = pop.set
            item.overwriteText()

    def addXTuple(self):
        pop = QDMContentListWidgetTuplePopup(tuple(["", ""]), self.firstTupleType_comboBox.currentText())
        if pop.exec():
            newItem = QDMListWidgetItem(pop.tuple, "2-tuple")
            self.x_tuple.addItem(newItem)
            self.x_tuple.scrollToBottom()
            self.x_tuple_add.setVisible(False)

    def addYTuple(self):
        pop = QDMContentListWidgetTuplePopup(tuple(["", ""]), self.secondTupleType_comboBox.currentText())
        if pop.exec():
            newItem = QDMListWidgetItem(pop.tuple, "2-tuple")
            self.y_tuple.addItem(newItem)
            self.y_tuple.scrollToBottom()
            self.y_tuple_add.setVisible(False)

    def addXSet(self):
        from fixpointtool.content.fpt_content_listWidget_inner_set_popup import QDMContentListWidgetInnerSetPopup
        pop = QDMContentListWidgetInnerSetPopup(set(), self.firstSetType_comboBox.currentText())
        if pop.exec():
            newItem = QDMListWidgetItem(pop.set, "set")
            self.x_set.addItem(newItem)
            self.x_set.scrollToBottom()
            self.x_set_add.setVisible(False)

    def addYSet(self):
        from fixpointtool.content.fpt_content_listWidget_inner_set_popup import QDMContentListWidgetInnerSetPopup
        pop = QDMContentListWidgetInnerSetPopup(set(), self.secondSetType_comboBox.currentText())
        if pop.exec():
            newItem = QDMListWidgetItem(pop.set, "set")
            self.y_set.addItem(newItem)
            self.y_set.scrollToBottom()
            self.y_set_add.setVisible(False)

    def onSave(self):
        if self.type_of_tuple == "string":
            self.tuple = (self.x_value.toPlainText(), self.y_value.toPlainText())
            self.accept()
        elif self.type_of_tuple == "number":
            try:
                self.tuple = (float(self.x_value.toPlainText()), float(self.y_value.toPlainText()))
                self.accept()
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nThere are inputs of a wrong type")
                msg.exec()
        elif self.type_of_tuple == "mapping":
            if self.x_mapping.count() > 0 and self.y_mapping.count() > 0:
                self.tuple = (FPTMapping(self.x_mapping.currentText()), FPTMapping(self.y_mapping.currentText()))
            else:
                self.tuple = (None, None)
            self.accept()
        elif self.type_of_tuple == "set":
            if self.x_set.count() > 0 and self.y_set.count() > 0:
                self.tuple = (self.x_set.item(0).item, self.y_set.item(0).item)
                self.accept()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nSome inputs are missing")
                msg.exec()
        elif self.type_of_tuple == "2-tuple":
            if self.x_tuple.count() > 0 and self.y_tuple.count() > 0:
                self.tuple = (self.x_tuple.item(0).item, self.y_tuple.item(0).item)
                self.accept()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nSome inputs are missing")
                msg.exec()

    def onCancel(self):
        self.reject()